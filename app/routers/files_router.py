from quart import Blueprint, render_template

files_router = Blueprint("files", __name__)


@files_router.get("/")
async def files_page():
    return await render_template("pages/files.html")
