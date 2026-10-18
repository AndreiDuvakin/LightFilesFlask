import asyncio
import datetime
import math
from pathlib import Path
import re

import aiofiles
from quart import jsonify, redirect, url_for

from app.core.settings import settings
from app.db.session import get_db
from app.models.file_model import FileModel
from app.services.files_service import FilesService

merge_semaphore = asyncio.Semaphore(2)


class UploadController:
    async def upload_chunk(
        self,
        identifier,
        chunk_number,
        total_chunks,
        total_size,
        chunk_size,
        files,
        filename,
    ):
        from app.main import COMPLETED_DIR

        try:
            upload_dir = self.get_upload_dir(identifier)

            number = int(chunk_number)
            total = int(total_chunks)
            size = int(total_size)
            nominal_chunk_size = int(chunk_size)

            if (
                number < 1
                or total < 1
                or number > total
                or size < 1
                or size > settings.MAX_CONTENT_LENGTH
                or nominal_chunk_size < 1
                or total != math.ceil(size / nominal_chunk_size)
            ):
                raise ValueError

        except (ValueError, TypeError):
            return jsonify(error="Некорректные параметры загрузки"), 400

        uploaded_file = files.get("file")

        if uploaded_file is None:
            return jsonify(error="Чанк не найден"), 400

        upload_dir.mkdir(parents=True, exist_ok=True)

        chunk_path = upload_dir / f"chunk_{number:08d}"
        temp_path = upload_dir / f"chunk_{number:08d}.tmp"

        await uploaded_file.save(temp_path)
        temp_path.replace(chunk_path)

        async with merge_semaphore:
            if all(
                (upload_dir / f"chunk_{i:08d}").is_file() for i in range(1, total + 1)
            ):
                output_path = COMPLETED_DIR / filename

                async with aiofiles.open(output_path, "wb") as output:
                    for i in range(1, total + 1):
                        path = upload_dir / f"chunk_{i:08d}"

                        async with aiofiles.open(path, "rb") as chunk:
                            while data := await chunk.read(1024 * 1024):
                                await output.write(data)

                if output_path.stat().st_size != size:
                    output_path.unlink(missing_ok=True)
                    return jsonify(error="Размер файла не совпадает"), 400

                for path in upload_dir.iterdir():
                    path.unlink(missing_ok=True)

                upload_dir.rmdir()

                try:
                    async with get_db() as db:
                        files_service = FilesService(db)

                        new_file = FileModel(
                            filename=str(filename),
                            uploaded_at=datetime.datetime.now(),
                            size=size,
                        )

                        await files_service.create_file(new_file)

                except Exception:
                    output_path.unlink(missing_ok=True)

        return redirect(
            url_for("files.files_page"),
        )

    async def get_chunk_info(
        self,
        identifier,
        chunk_number,
    ):
        try:
            upload_dir = self.get_upload_dir(identifier)
            number = int(chunk_number)

            if number < 1:
                raise ValueError

        except ValueError:
            return "", 400

        chunk_path = upload_dir / f"chunk_{number:08d}"

        if chunk_path.is_file():
            return "", 200

        return "", 204

    @staticmethod
    def get_upload_dir(identifier: str) -> Path:
        from app.main import CHUNKS_DIR

        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,200}", identifier):
            raise ValueError("Некорректный идентификатор загрузки")

        return CHUNKS_DIR / identifier
