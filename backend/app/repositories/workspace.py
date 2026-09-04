from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workspace import Workspace


class WorkspaceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_workspaces(self) -> Sequence[Workspace]:
        result = await self._session.execute(select(Workspace).order_by(Workspace.created_at.asc()))
        return result.scalars().all()
