from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class QualityIssueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    column_name: str | None
    code: str
    severity: str
    message: str
    details: dict[str, Any]


class FieldProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    null_count: int
    null_percentage: float
    unique_count: int
    numeric_min: float | None
    numeric_max: float | None
    numeric_mean: float | None
    date_min: str | None
    date_max: str | None
    sample_values: list[Any]


class ColumnRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    position: int
    inferred_type: str
    generic_role: str
    profile: FieldProfileRead


class VersionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    version_number: int
    file_size: int
    row_count: int
    column_count: int
    duplicate_row_count: int
    created_at: datetime


class DatasetSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


class SourceRead(BaseModel):
    id: str
    name: str
    source_type: str
    original_filename: str
    status: str
    created_at: datetime
    updated_at: datetime
    dataset: DatasetSummary
    latest_version: VersionSummary
    quality_issue_count: int


class DatasetDetail(BaseModel):
    id: str
    source_id: str
    name: str
    source_type: str
    original_filename: str
    created_at: datetime
    updated_at: datetime
    latest_version: VersionSummary
    quality_issue_count: int


class VersionDetail(VersionSummary):
    columns: list[ColumnRead]
    quality_issues: list[QualityIssueRead]


class ProfileRead(BaseModel):
    dataset_id: str
    version: VersionDetail


class PreviewRead(BaseModel):
    dataset_id: str
    version_id: str
    columns: list[str]
    rows: list[dict[str, Any]]
    limit: int
