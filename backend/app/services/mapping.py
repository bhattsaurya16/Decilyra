from __future__ import annotations

import re
from difflib import SequenceMatcher

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import DecilyraError
from app.domain.canonical_fields.catalog import CANONICAL_FIELDS
from app.models.dataset import Dataset, DatasetVersion, SourceColumn
from app.models.mapping import CanonicalField, FieldMapping

AMBIGUOUS_NAMES = {"amount", "total", "value", "cost", "date", "id", "sales", "revenue", "discount"}
DEFINITION_SENSITIVE = {"GROSS_REVENUE", "NET_REVENUE", "DISCOUNT_AMOUNT", "DISCOUNT_RATE"}
NUMERIC_TYPES = {"integer", "decimal"}


def normalize(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


async def seed_catalog(session: AsyncSession) -> list[CanonicalField]:
    existing = {item.code: item for item in (await session.execute(select(CanonicalField))).scalars().all()}
    changed = False
    for definition in CANONICAL_FIELDS:
        item = existing.get(definition["code"])
        if item is None:
            item = CanonicalField(**definition, examples=[], active=True)
            session.add(item)
            existing[item.code] = item
            changed = True
    if changed:
        await session.commit()
    return sorted(existing.values(), key=lambda item: (item.domain, item.code))


class MappingService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _dataset(self, dataset_id: str) -> tuple[Dataset, DatasetVersion]:
        result = await self.session.execute(
            select(Dataset).where(Dataset.id == dataset_id).options(selectinload(Dataset.versions).selectinload(DatasetVersion.columns).selectinload(SourceColumn.profile))
        )
        dataset = result.scalar_one_or_none()
        if not dataset or not dataset.versions:
            raise DecilyraError("Dataset not found.", 404, "dataset_not_found")
        return dataset, max(dataset.versions, key=lambda item: item.version_number)

    async def suggest(self, dataset_id: str) -> list[FieldMapping]:
        catalog = await seed_catalog(self.session)
        _, version = await self._dataset(dataset_id)
        existing_result = await self.session.execute(select(FieldMapping).where(FieldMapping.dataset_version_id == version.id))
        existing = {item.source_column_id: item for item in existing_result.scalars().all()}
        context_names = {normalize(column.name) for column in version.columns}
        for column in version.columns:
            current = existing.get(column.id)
            if current and (current.mapping_method == "USER" or current.status in {"CONFIRMED", "REJECTED"}):
                continue
            candidates = [self._score(column, item, context_names) for item in catalog if item.active]
            candidates.sort(key=lambda item: item[0], reverse=True)
            score, canonical, evidence = candidates[0]
            alternatives = [{"canonical_field_id": item.id, "code": item.code, "score": round(candidate_score, 2)} for candidate_score, item, _ in candidates[:3] if candidate_score >= 0.35]
            normalized = normalize(column.name)
            if score < 0.48:
                status, canonical_id, level = "UNMAPPED", None, None
            elif normalized in AMBIGUOUS_NAMES or canonical.code in DEFINITION_SENSITIVE or score < 0.8:
                status, canonical_id, level = "NEEDS_REVIEW", canonical.id, self._level(score)
            else:
                status, canonical_id, level = "SUGGESTED", canonical.id, self._level(score)
            mapping = current or FieldMapping(dataset_version_id=version.id, source_column_id=column.id)
            mapping.canonical_field_id = canonical_id
            mapping.status = status
            mapping.confidence = round(score, 2) if canonical_id else None
            mapping.confidence_level = level
            mapping.mapping_method = "HEURISTIC"
            mapping.evidence = evidence if canonical_id else [{"kind": "info", "message": "No sufficiently strong deterministic match was found."}]
            mapping.alternatives = alternatives
            mapping.confirmed_by_user = False
            mapping.grain = canonical.expected_grain if canonical_id else "UNKNOWN"
            if current is None:
                self.session.add(mapping)
        await self.session.commit()
        return await self.list_for_dataset(dataset_id)

    def _score(self, column: SourceColumn, canonical: CanonicalField, context_names: set[str]) -> tuple[float, CanonicalField, list[dict[str, str]]]:
        name = normalize(column.name)
        aliases = {normalize(alias) for alias in canonical.aliases} | {normalize(canonical.code), normalize(canonical.name)}
        exact = name in aliases
        similarity = max(SequenceMatcher(None, name, alias).ratio() for alias in aliases)
        score = 0.0
        evidence: list[dict[str, str]] = []
        if exact:
            score += 0.64
            evidence.append({"kind": "positive", "message": f'Column name matches the known alias "{name}".'})
        elif similarity >= 0.72:
            score += similarity * 0.48
            evidence.append({"kind": "positive", "message": "Normalized column name is similar to a catalog alias."})
        compatible = self._compatible(column.inferred_type, canonical.expected_data_type, canonical.unit_type)
        if compatible:
            score += 0.18
            evidence.append({"kind": "positive", "message": f"Detected {column.inferred_type} type is compatible with the canonical definition."})
        elif canonical.unit_type in {"CURRENCY", "COUNT", "PERCENTAGE", "QUANTITY", "HOURS", "RATE"}:
            score -= 0.35
            evidence.append({"kind": "warning", "message": f"Detected {column.inferred_type} type conflicts with a numeric canonical field."})
        role_support = (canonical.unit_type == "IDENTIFIER" and column.generic_role == "possible_id") or (canonical.unit_type == "DATE" and column.generic_role == "possible_date") or (canonical.unit_type in {"CURRENCY", "COUNT", "PERCENTAGE", "QUANTITY", "HOURS", "RATE"} and column.generic_role == "possible_numeric_measure") or (canonical.unit_type == "CATEGORY" and column.generic_role == "possible_category")
        if role_support:
            score += 0.1
            evidence.append({"kind": "positive", "message": f"Profile role {column.generic_role} supports this meaning."})
        has_order_context = bool(context_names & {"order_id", "invoice_id", "transaction_id"}) and bool(context_names & {"order_date", "invoice_date", "transaction_date", "date"})
        sales_context = len(context_names & {"order_id", "transaction_id", "quantity", "product", "product_category", "price_per_unit", "unit_price", "total_amount", "sales_amount"}) >= 2
        accounting_context = bool(context_names & {"account_id", "account_code", "journal_entry_id", "debit", "credit", "gl_account"})
        if canonical.code == "ORDER_DATE" and name == "date" and sales_context:
            score += 0.25
            evidence.append({"kind": "positive", "message": "Sales and transaction fields make an order date plausible."})
        if canonical.code == "POSTING_DATE" and not accounting_context:
            score -= 0.2
            evidence.append({"kind": "warning", "message": "No journal or account fields support an accounting posting date."})
        if canonical.code in {"NET_REVENUE", "GROSS_REVENUE"} and has_order_context:
            score += 0.07
            evidence.append({"kind": "positive", "message": "Related order identifier and date fields are present."})
        if canonical.unit_type == "CURRENCY":
            evidence.append({"kind": "warning", "message": "Currency code is unknown; no currency is assumed."})
        if canonical.code in {"NET_REVENUE", "GROSS_REVENUE"}:
            evidence.append({"kind": "warning", "message": "Whether discounts, returns, and allowances are included cannot be proven from profiling alone."})
        if name == "discount" and canonical.code == "DISCOUNT_RATE" and column.profile and column.profile.numeric_max is not None:
            if 0 <= (column.profile.numeric_min or 0) and column.profile.numeric_max <= 1:
                score += 0.06
                evidence.append({"kind": "positive", "message": "Observed values fall between 0 and 1, consistent with a fractional rate."})
            else:
                score -= 0.15
                evidence.append({"kind": "warning", "message": "Observed values do not clearly establish a fractional discount rate."})
        if not exact and not compatible:
            score = min(score, 0.45)
        return max(0.0, min(score, 0.99)), canonical, evidence

    @staticmethod
    def _compatible(actual: str, expected: str, unit: str) -> bool:
        if unit == "IDENTIFIER":
            return actual in {"integer", "text", "categorical"}
        if expected in NUMERIC_TYPES:
            return actual in NUMERIC_TYPES
        if expected in {"date", "datetime"}:
            return actual in {"date", "datetime"}
        if expected == "categorical":
            return actual in {"categorical", "text"}
        return actual in {"text", "categorical"}

    @staticmethod
    def _level(score: float) -> str:
        return "HIGH" if score >= 0.8 else "MEDIUM" if score >= 0.6 else "LOW"

    async def list_for_dataset(self, dataset_id: str) -> list[FieldMapping]:
        _, version = await self._dataset(dataset_id)
        result = await self.session.execute(select(FieldMapping).where(FieldMapping.dataset_version_id == version.id).options(selectinload(FieldMapping.source_column).selectinload(SourceColumn.profile), selectinload(FieldMapping.canonical_field)).order_by(FieldMapping.created_at))
        return list(result.scalars().all())

    async def get(self, mapping_id: str) -> FieldMapping:
        result = await self.session.execute(select(FieldMapping).where(FieldMapping.id == mapping_id).options(selectinload(FieldMapping.source_column).selectinload(SourceColumn.profile), selectinload(FieldMapping.canonical_field)))
        mapping = result.scalar_one_or_none()
        if not mapping:
            raise DecilyraError("Mapping not found.", 404, "mapping_not_found")
        return mapping

    async def update(self, mapping_id: str, status: str, canonical_field_id: str | None = None) -> FieldMapping:
        mapping = await self.get(mapping_id)
        allowed = {"SUGGESTED", "CONFIRMED", "REJECTED", "UNMAPPED", "NEEDS_REVIEW"}
        if status not in allowed:
            raise DecilyraError("Invalid mapping status.", 422, "invalid_mapping_status")
        if canonical_field_id is not None:
            canonical = await self.session.get(CanonicalField, canonical_field_id)
            if not canonical or not canonical.active:
                raise DecilyraError("Canonical field not found.", 404, "canonical_field_not_found")
            mapping.canonical_field_id = canonical.id
            mapping.canonical_field = canonical
            mapping.grain = canonical.expected_grain
            mapping.mapping_method = "USER"
        if status == "CONFIRMED" and not mapping.canonical_field_id:
            raise DecilyraError("Choose a canonical field before confirming.", 422, "canonical_field_required")
        if status == "UNMAPPED":
            mapping.canonical_field_id = None
            mapping.confidence = None
            mapping.confidence_level = None
            mapping.grain = "UNKNOWN"
        mapping.status = status
        mapping.confirmed_by_user = status == "CONFIRMED"
        if status in {"CONFIRMED", "REJECTED", "UNMAPPED"}:
            mapping.mapping_method = "USER"
        await self.session.commit()
        return await self.get(mapping.id)
