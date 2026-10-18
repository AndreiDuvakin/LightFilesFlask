from quart import Blueprint

from app.controllers.download_controller import DownloadController

download_router = Blueprint("download", __name__)


@download_router.get('/download/<int:file_id>')
async def download_file(file_id: int):
    return await DownloadController.download_file(file_id)
