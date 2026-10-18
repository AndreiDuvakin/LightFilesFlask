import asyncio
from pathlib import Path

from quart import Quart
from quart_auth import QuartAuth

from app.core.settings import settings
from app.db.session import init_db
from app.routers.files_router import files_router
from app.routers.login_router import login_router
from app.utils.create_admin_user import create_admin_user
from app.models.auth_model import AuthModel
from app.routers.logout_router import logout_router
from app.routers.upload_router import upload_router

UPLOAD_DIR = Path("uploads/")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

CHUNKS_DIR = UPLOAD_DIR / "chunks"
COMPLETED_DIR = UPLOAD_DIR / "completed"


async def main():
    app = Quart(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["QUART_AUTH_COOKIE_SECURE"] = not settings.DEBUG
    app.config['MAX_CONTENT_LENGTH'] = settings.MAX_CONTENT_LENGTH

    await init_db()
    await create_admin_user()

    auth_manager = QuartAuth()
    auth_manager.user_class = AuthModel
    auth_manager.init_app(app)

    register_app_blueprints(app)
    make_context(app)
    make_prepare_upload_dirs(app)

    await app.run_task(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.DEBUG,
    )


def make_prepare_upload_dirs(app):
    @app.before_serving
    async def prepare_upload_dirs():
        CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
        COMPLETED_DIR.mkdir(parents=True, exist_ok=True)


def make_context(app):
    @app.context_processor
    def inject_globals():
        return {
            "prefix": settings.PREFIX,
        }


def register_app_blueprints(app):
    app.register_blueprint(files_router, url_prefix=settings.PREFIX)
    app.register_blueprint(login_router, url_prefix=settings.PREFIX)
    app.register_blueprint(logout_router, url_prefix=settings.PREFIX)
    app.register_blueprint(upload_router, url_prefix=settings.PREFIX)


if __name__ == "__main__":
    asyncio.run(main())
