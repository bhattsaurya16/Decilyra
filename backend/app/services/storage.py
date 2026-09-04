from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from uuid import uuid4


class StorageService(ABC):
    @abstractmethod
    async def save(self, content: bytes) -> str: ...

    @abstractmethod
    async def read(self, key: str) -> bytes: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...


class LocalStorageService(StorageService):
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        if Path(key).name != key:
            raise ValueError("Invalid storage key")
        path = (self.root / key).resolve()
        if path.parent != self.root:
            raise ValueError("Invalid storage key")
        return path

    async def save(self, content: bytes) -> str:
        key = f"{uuid4().hex}.csv"
        self._path(key).write_bytes(content)
        return key

    async def read(self, key: str) -> bytes:
        return self._path(key).read_bytes()

    async def delete(self, key: str) -> None:
        self._path(key).unlink(missing_ok=True)
