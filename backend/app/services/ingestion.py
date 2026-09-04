from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DecilyraError
from app.models.dataset import DataSource, Dataset, DatasetVersion, FieldProfile, QualityIssue, SourceColumn
from app.repositories.datasets import DatasetRepository
from app.services.profiler import DatasetProfile, parse_csv, profile_csv
from app.services.storage import StorageService


class IngestionService:
    def __init__(self, session: AsyncSession, storage: StorageService, max_bytes: int) -> None:
        self.session = session
        self.storage = storage
        self.max_bytes = max_bytes
        self.repository = DatasetRepository(session)

    async def upload(self, filename: str | None, content: bytes) -> DataSource:
        safe_name = Path(filename or "").name
        if not safe_name or Path(safe_name).suffix.lower() != ".csv":
            raise DecilyraError("Only .csv files are supported.", 415, "invalid_file_type")
        if len(content) > self.max_bytes:
            raise DecilyraError("The upload exceeds the configured size limit.", 413, "file_too_large")
        try:
            profile = profile_csv(content)
        except ValueError as exc:
            raise DecilyraError(str(exc), 422, "invalid_csv") from exc
        storage_key = await self.storage.save(content)
        try:
            source = self._build_models(safe_name, len(content), storage_key, profile)
            self.session.add(source)
            await self.session.commit()
            loaded = await self.repository.get_source(source.id)
            assert loaded is not None
            return loaded
        except Exception:
            await self.session.rollback()
            await self.storage.delete(storage_key)
            raise

    @staticmethod
    def _build_models(filename: str, file_size: int, storage_key: str, result: DatasetProfile) -> DataSource:
        name = Path(filename).stem
        source = DataSource(name=name, original_filename=filename, source_type="csv", status="ready")
        dataset = Dataset(name=name)
        version = DatasetVersion(version_number=1, storage_key=storage_key, file_size=file_size, row_count=len(result.dataframe), column_count=len(result.dataframe.columns), duplicate_row_count=result.duplicate_row_count)
        dataset.versions.append(version)
        source.dataset = dataset
        for item in result.columns:
            column = SourceColumn(name=item.name, position=item.position, inferred_type=item.inferred_type, generic_role=item.generic_role)
            column.profile = FieldProfile(null_count=item.null_count, null_percentage=item.null_percentage, unique_count=item.unique_count, numeric_min=item.numeric_min, numeric_max=item.numeric_max, numeric_mean=item.numeric_mean, date_min=item.date_min, date_max=item.date_max, sample_values=item.sample_values)
            version.columns.append(column)
        for item in result.issues:
            version.quality_issues.append(QualityIssue(column_name=item.column_name, code=item.code, severity=item.severity, message=item.message, details=item.details))
        return source

    async def preview(self, dataset_id: str, limit: int) -> tuple[DatasetVersion, list[str], list[dict[str, Any]]]:
        dataset = await self.repository.get_dataset(dataset_id)
        if not dataset or not dataset.versions:
            raise DecilyraError("Dataset not found.", 404, "dataset_not_found")
        version = max(dataset.versions, key=lambda item: item.version_number)
        content = await self.storage.read(version.storage_key)
        frame, _ = parse_csv(content)
        preview = frame.head(limit).astype(object).where(pd.notna(frame.head(limit)), None)
        rows = [{str(key): self._plain(value) for key, value in row.items()} for row in preview.to_dict(orient="records")]
        return version, [str(column) for column in frame.columns], rows

    @staticmethod
    def _plain(value: Any) -> Any:
        if hasattr(value, "item"):
            return value.item()
        return value
