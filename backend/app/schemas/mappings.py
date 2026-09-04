from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.datasets import ColumnRead

MappingStatus = Literal["SUGGESTED", "CONFIRMED", "REJECTED", "UNMAPPED", "NEEDS_REVIEW"]


class CanonicalFieldRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    code: str
    domain: str
    name: str
    description: str
    expected_data_type: str
    expected_grain: str
    unit_type: str
    entity_type: str
    aliases: list[str]
    active: bool


class MappingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    dataset_version_id: str
    source_column_id: str
    status: str
    confidence: float | None
    confidence_level: str | None
    mapping_method: str
    evidence: list[dict[str, str]]
    alternatives: list[dict[str, Any]]
    confirmed_by_user: bool
    grain: str
    created_at: datetime
    updated_at: datetime
    source_column: ColumnRead
    canonical_field: CanonicalFieldRead | None


class MappingUpdate(BaseModel):
    status: MappingStatus
    canonical_field_id: str | None = None


class MappingChoice(BaseModel):
    canonical_field_id: str | None = None


class DomainCoverage(BaseModel):
    domain: str
    confirmed_fields: int
    catalog_fields: int
    status: Literal["PARTIAL", "MISSING"]


class MappingSummary(BaseModel):
    total: int
    confirmed: int
    needs_review: int
    suggested: int
    rejected: int
    unmapped: int
    domains: list[DomainCoverage]


class MappingCollection(BaseModel):
    dataset_id: str
    dataset_version_id: str
    mappings: list[MappingRead]
    summary: MappingSummary
