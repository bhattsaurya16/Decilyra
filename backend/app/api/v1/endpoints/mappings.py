from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.datasets import DbSession
from app.domain.canonical_fields.catalog import CANONICAL_FIELDS
from app.models.mapping import FieldMapping
from app.schemas.mappings import CanonicalFieldRead, DomainCoverage, MappingChoice, MappingCollection, MappingRead, MappingSummary, MappingUpdate
from app.services.mapping import MappingService, seed_catalog

router = APIRouter()


def collection(dataset_id: str, mappings: list[FieldMapping]) -> MappingCollection:
    statuses = [item.status for item in mappings]
    confirmed_by_domain: dict[str, int] = {}
    catalog_by_domain: dict[str, set[str]] = {}
    for definition in CANONICAL_FIELDS:
        catalog_by_domain.setdefault(definition["domain"], set()).add(definition["code"])
    for item in mappings:
        if item.canonical_field:
            if item.status == "CONFIRMED":
                confirmed_by_domain[item.canonical_field.domain] = confirmed_by_domain.get(item.canonical_field.domain, 0) + 1
    domains = [DomainCoverage(domain=domain, confirmed_fields=confirmed_by_domain.get(domain, 0), catalog_fields=len(codes), status="PARTIAL" if confirmed_by_domain.get(domain, 0) else "MISSING") for domain, codes in sorted(catalog_by_domain.items())]
    summary = MappingSummary(total=len(mappings), confirmed=statuses.count("CONFIRMED"), needs_review=statuses.count("NEEDS_REVIEW"), suggested=statuses.count("SUGGESTED"), rejected=statuses.count("REJECTED"), unmapped=statuses.count("UNMAPPED"), domains=domains)
    version_id = mappings[0].dataset_version_id if mappings else ""
    return MappingCollection(dataset_id=dataset_id, dataset_version_id=version_id, mappings=[MappingRead.model_validate(item) for item in mappings], summary=summary)


@router.get("/canonical-fields", response_model=list[CanonicalFieldRead])
async def list_canonical_fields(session: DbSession) -> list[CanonicalFieldRead]:
    return [CanonicalFieldRead.model_validate(item) for item in await seed_catalog(session)]


@router.post("/datasets/{dataset_id}/mappings/suggest", response_model=MappingCollection)
async def suggest_mappings(dataset_id: str, session: DbSession) -> MappingCollection:
    return collection(dataset_id, await MappingService(session).suggest(dataset_id))


@router.get("/datasets/{dataset_id}/mappings", response_model=MappingCollection)
async def list_mappings(dataset_id: str, session: DbSession) -> MappingCollection:
    return collection(dataset_id, await MappingService(session).list_for_dataset(dataset_id))


@router.patch("/mappings/{mapping_id}", response_model=MappingRead)
async def update_mapping(mapping_id: str, payload: MappingUpdate, session: DbSession) -> MappingRead:
    return MappingRead.model_validate(await MappingService(session).update(mapping_id, payload.status, payload.canonical_field_id))


@router.post("/mappings/{mapping_id}/confirm", response_model=MappingRead)
async def confirm_mapping(mapping_id: str, payload: MappingChoice, session: DbSession) -> MappingRead:
    return MappingRead.model_validate(await MappingService(session).update(mapping_id, "CONFIRMED", payload.canonical_field_id))


@router.post("/mappings/{mapping_id}/reject", response_model=MappingRead)
async def reject_mapping(mapping_id: str, session: DbSession) -> MappingRead:
    return MappingRead.model_validate(await MappingService(session).update(mapping_id, "REJECTED"))
