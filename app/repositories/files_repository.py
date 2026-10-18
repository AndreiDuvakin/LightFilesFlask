from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.entities.files import File


class FilesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_file_by_id(self, file_id: int) -> File | None:
        query = select(File).filter_by(id=file_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(self) -> Sequence[Any]:
        query = select(File)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_file(self, file: File) -> File:
        self.db.add(file)
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def delete_file(self, file: File) -> File:
        await self.db.delete(file)
        await self.db.commit()
        return file
