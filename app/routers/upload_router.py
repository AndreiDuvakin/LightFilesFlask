from quart import Blueprint, render_template, request
from quart_auth import login_required

from app.controllers.upload_controller import UploadController

upload_router = Blueprint("upload", __name__)


@upload_router.get("/upload")
@login_required
async def upload_page():
    return await render_template("pages/upload.html")


@upload_router.get("/api/upload")
@login_required
async def get_chunk_info():
    identifier = request.args.get("resumableIdentifier", "")
    chunk_number = request.args.get("resumableChunkNumber", "")

    upload_controller = UploadController()

    return await upload_controller.get_chunk_info(
        identifier,
        chunk_number,
    )


@upload_router.post("/api/upload")
@login_required
async def upload_chunk():
    form = await request.form
    files = await request.files

    identifier = form.get("resumableIdentifier", "")
    filename = form.get("resumableFilename", "")
    chunk_number = form.get("resumableChunkNumber", "")
    total_chunks = form.get("resumableTotalChunks", "")
    total_size = form.get("resumableTotalSize", "")
    chunk_size = form.get("resumableChunkSize", "")

    upload_controller = UploadController()

    return await upload_controller.upload_chunk(
        identifier,
        chunk_number,
        total_chunks,
        total_size,
        chunk_size,
        files,
        filename,
    )
