from typing import Any, List, Sequence

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

    async def create_list_files(self, files: List[File]) -> Sequence[File]:
        self.db.add_all(files)
        await self.db.commit()

        for file in files:
            await self.db.refresh(file)

        return files

    async def delete_file(self, file: File) -> File:
        await self.db.delete(file)
        await self.db.commit()
        return file
