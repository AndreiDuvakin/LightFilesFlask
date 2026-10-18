from typing import List

from app.models.file_model import FileModel
from app.repositories.files_repository import FilesRepository


class FilesService:
    def __init__(self, db):
        self.files_repository = FilesRepository(db)

    async def get_all_files(self) -> List[FileModel]:
        files = await self.files_repository.get_all()

        return [FileModel.from_entity(file) for file in files]

    async def get_file_by_id(self, file_id: int) -> FileModel | None:
        file = await self.files_repository.get_file_by_id(file_id)

        if not file:
            return None

        return FileModel.from_entity(file)

    async def create_file(
            self,
            file: FileModel,
    ) -> FileModel:
        file_entity = file.to_entity()

        file_model = await self.files_repository.create_file(
            file_entity,
        )

        return FileModel.from_entity(file_model)

    async def delete_file(self, file_id: int) -> FileModel | None:
        file_entity = await self.files_repository.get_file_by_id(file_id)

        if not file_entity:
            return None

        file_entity = await self.files_repository.delete_file(file_entity)

        return FileModel.from_entity(file_entity)
