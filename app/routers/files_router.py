from quart import Blueprint
from quart_auth import login_required

from app.controllers.files_page_controller import FilesPageController

files_router = Blueprint("files", __name__)


@files_router.get("/")
async def files_page():
    return await FilesPageController.get_all_files()


@files_router.get("/delete/<int:file_id>")
@login_required
async def delete_file(file_id: int):
    return await FilesPageController.delete_file(file_id)
