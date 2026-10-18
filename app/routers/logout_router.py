from quart import Blueprint, redirect, url_for
from quart_auth import login_required, logout_user

logout_router = Blueprint("logout", __name__)


@logout_router.route("/logout")
@login_required
async def logout():
    logout_user()
    return redirect(
        url_for("files.files_page"),
    )
