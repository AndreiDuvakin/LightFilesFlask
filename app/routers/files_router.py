from quart import Blueprint, request
from quart_auth import login_required

from app.controllers.files_page_controller import FilesPageController

files_router = Blueprint("files", __name__)


@files_router.get("/")
async def files_page():
    args = request.args

    message = args.get("message", None)
    success = args.get("success", False)

    return await FilesPageController.get_all_files(
        message,
        success,
    )


@files_router.post("/delete/<int:file_id>")
@login_required
async def delete_file(file_id: int):
    return await FilesPageController.delete_file(file_id)
