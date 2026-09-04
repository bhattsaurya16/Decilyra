import asyncio
from collections.abc import AsyncIterator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.core.database import Base, get_db_session
from app.main import app
from app.models import CanonicalField, DataSource, Dataset, DatasetVersion, FieldMapping, FieldProfile, QualityIssue, SourceColumn, Workspace  # noqa: F401


@pytest.fixture
def client(tmp_path, monkeypatch) -> Generator[TestClient, None, None]:
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'test.db'}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    get_settings.cache_clear()
    engine = create_async_engine(database_url)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async def setup() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    async def override_session() -> AsyncIterator:
        async with factory() as session:
            yield session
    asyncio.run(setup())
    app.dependency_overrides[get_db_session] = override_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    asyncio.run(engine.dispose())
    get_settings.cache_clear()
