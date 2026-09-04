from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, Query, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db_session
from app.core.exceptions import DecilyraError
from app.models.dataset import DataSource, Dataset, DatasetVersion
from app.repositories.datasets import DatasetRepository
from app.schemas.datasets import DatasetDetail, PreviewRead, ProfileRead, SourceRead, VersionDetail, VersionSummary
from app.services.ingestion import IngestionService
from app.services.storage import LocalStorageService

router = APIRouter()
DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def service(session: AsyncSession) -> IngestionService:
    settings = get_settings()
    return IngestionService(session, LocalStorageService(settings.upload_dir), settings.max_upload_size_mb * 1024 * 1024)


def latest(dataset: Dataset) -> DatasetVersion:
    if not dataset.versions:
        raise DecilyraError("Dataset has no versions.", 500, "dataset_has_no_versions")
    return max(dataset.versions, key=lambda item: item.version_number)


def source_read(source: DataSource) -> SourceRead:
    version = latest(source.dataset)
    return SourceRead(
        id=source.id, name=source.name, source_type=source.source_type, original_filename=source.original_filename,
        status=source.status, created_at=source.created_at, updated_at=source.updated_at,
        dataset=source.dataset, latest_version=version, quality_issue_count=len(version.quality_issues),
    )


def dataset_read(dataset: Dataset) -> DatasetDetail:
    version = latest(dataset)
    return DatasetDetail(
        id=dataset.id, source_id=dataset.source_id, name=dataset.name, source_type=dataset.source.source_type,
        original_filename=dataset.source.original_filename, created_at=dataset.created_at, updated_at=dataset.updated_at,
        latest_version=version, quality_issue_count=len(version.quality_issues),
    )


@router.post("/sources/upload", response_model=SourceRead, status_code=201)
async def upload_source(file: Annotated[UploadFile, File(...)], session: DbSession) -> SourceRead:
    settings = get_settings()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    content = await file.read(max_bytes + 1)
    return source_read(await service(session).upload(file.filename, content))


@router.get("/sources", response_model=list[SourceRead])
async def list_sources(session: DbSession) -> list[SourceRead]:
    return [source_read(item) for item in await DatasetRepository(session).list_sources()]


@router.get("/sources/{source_id}", response_model=SourceRead)
async def get_source(source_id: str, session: DbSession) -> SourceRead:
    source = await DatasetRepository(session).get_source(source_id)
    if not source:
        raise DecilyraError("Source not found.", 404, "source_not_found")
    return source_read(source)


@router.delete("/sources/{source_id}", status_code=204)
async def delete_source(source_id: str, session: DbSession) -> Response:
    source = await DatasetRepository(session).get_source(source_id)
    if not source:
        raise DecilyraError("Source not found.", 404, "source_not_found")
    keys = [version.storage_key for version in source.dataset.versions]
    await session.delete(source)
    await session.commit()
    storage = service(session).storage
    for key in keys:
        await storage.delete(key)
    return Response(status_code=204)


@router.get("/datasets/{dataset_id}", response_model=DatasetDetail)
async def get_dataset(dataset_id: str, session: DbSession) -> DatasetDetail:
    dataset = await DatasetRepository(session).get_dataset(dataset_id)
    if not dataset:
        raise DecilyraError("Dataset not found.", 404, "dataset_not_found")
    return dataset_read(dataset)


@router.get("/datasets/{dataset_id}/versions", response_model=list[VersionSummary])
async def list_versions(dataset_id: str, session: DbSession) -> list[DatasetVersion]:
    dataset = await DatasetRepository(session).get_dataset(dataset_id)
    if not dataset:
        raise DecilyraError("Dataset not found.", 404, "dataset_not_found")
    return sorted(dataset.versions, key=lambda item: item.version_number, reverse=True)


@router.get("/datasets/{dataset_id}/versions/{version_id}", response_model=VersionDetail)
async def get_version(dataset_id: str, version_id: str, session: DbSession) -> DatasetVersion:
    version = await DatasetRepository(session).get_version(dataset_id, version_id)
    if not version:
        raise DecilyraError("Dataset version not found.", 404, "version_not_found")
    return version


@router.get("/datasets/{dataset_id}/versions/{version_id}/profile", response_model=ProfileRead)
async def get_profile(dataset_id: str, version_id: str, session: DbSession) -> ProfileRead:
    version = await DatasetRepository(session).get_version(dataset_id, version_id)
    if not version:
        raise DecilyraError("Dataset version not found.", 404, "version_not_found")
    return ProfileRead(dataset_id=dataset_id, version=VersionDetail.model_validate(version))


@router.get("/datasets/{dataset_id}/preview", response_model=PreviewRead)
async def preview_dataset(dataset_id: str, session: DbSession, limit: int = Query(50, ge=1, le=100)) -> PreviewRead:
    version, columns, rows = await service(session).preview(dataset_id, limit)
    return PreviewRead(dataset_id=dataset_id, version_id=version.id, columns=columns, rows=rows, limit=limit)
