from quart import render_template

from app.db.session import get_db
from app.services.files_service import FilesService


class FilesPageController:
    @staticmethod
    async def get_all_files():
        async with get_db() as db:
            files_service = FilesService(db)

            files = await files_service.get_all_files()

        return await render_template("pages/files_page.html", files=files)

    @staticmethod
    async def delete_file(file_id: int):
        from app.main import COMPLETED_DIR

        async with get_db() as db:
            files_service = FilesService(db)

            file = await files_service.get_file_by_id(file_id)

            if not file:
                return await render_template(
                    "pages/files_page.html",
                    message="Файл не найден",
                )

            output_path = COMPLETED_DIR / file.filename

            if not output_path.is_file():
                await files_service.delete_file(file_id)
                return await render_template(
                    "pages/files_page.html",
                    message="Файл не найден на диске",
                )

            try:
                output_path.unlink()
                await files_service.delete_file(file_id)

            except Exception as e:
                return await render_template(
                    "pages/files_page.html",
                    message="Ошибка при удалени файла",
                )

            return await render_template(
                "pages/files_page.html",
            )
