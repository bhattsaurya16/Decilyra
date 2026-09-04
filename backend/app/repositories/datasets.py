from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.dataset import DataSource, Dataset, DatasetVersion, SourceColumn


VERSION_LOADS = (
    selectinload(DatasetVersion.columns).selectinload(SourceColumn.profile),
    selectinload(DatasetVersion.quality_issues),
)


class DatasetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_sources(self) -> list[DataSource]:
        versions = selectinload(DataSource.dataset).selectinload(Dataset.versions)
        result = await self.session.execute(
            select(DataSource)
            .options(
                versions.selectinload(DatasetVersion.quality_issues),
                versions.selectinload(DatasetVersion.columns).selectinload(SourceColumn.profile),
            )
            .order_by(DataSource.updated_at.desc())
        )
        return list(result.scalars().all())

    async def get_source(self, source_id: str) -> DataSource | None:
        result = await self.session.execute(
            select(DataSource)
            .where(DataSource.id == source_id)
            .options(selectinload(DataSource.dataset).selectinload(Dataset.versions).options(*VERSION_LOADS))
        )
        return result.scalar_one_or_none()

    async def get_dataset(self, dataset_id: str) -> Dataset | None:
        result = await self.session.execute(
            select(Dataset)
            .where(Dataset.id == dataset_id)
            .options(selectinload(Dataset.source), selectinload(Dataset.versions).options(*VERSION_LOADS))
        )
        return result.scalar_one_or_none()

    async def get_version(self, dataset_id: str, version_id: str) -> DatasetVersion | None:
        result = await self.session.execute(
            select(DatasetVersion)
            .where(DatasetVersion.dataset_id == dataset_id, DatasetVersion.id == version_id)
            .options(*VERSION_LOADS)
        )
        return result.scalar_one_or_none()
