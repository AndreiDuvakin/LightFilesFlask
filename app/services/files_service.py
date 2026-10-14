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

    async def create_list_files(
        self,
        files: List[FileModel],
    ) -> List[FileModel]:
        files_entities = [file.to_entity() for file in files]

        files_models = await self.files_repository.create_list_files(
            files_entities,
        )

        return [FileModel.from_entity(file) for file in files_models]

    async def delete_file(self, file_id: int) -> FileModel | None:
        file_entity = await self.files_repository.get_file_by_id(file_id)

        if not file_entity:
            return None

        file_entity = await self.files_repository.delete_file(file_entity)

        return FileModel.from_entity(file_entity)
