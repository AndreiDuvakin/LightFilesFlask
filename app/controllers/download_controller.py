from quart import render_template, send_file

from app.db.session import get_db
from app.services.files_service import FilesService


class DownloadController:
    @staticmethod
    async def download_file(file_id: int):
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

            return await send_file(
                output_path,
                as_attachment=True,
                attachment_filename=file.filename,
            )
