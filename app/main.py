import asyncio
from datetime import timedelta
from pathlib import Path

from hypercorn.middleware import ProxyFixMiddleware
from quart import Quart
from quart_auth import QuartAuth
from quart_wtf import CSRFProtect

from app.core.chunk_cleanup import chunk_cleanup_loop, cleanup_old_chunks_once
from app.core.settings import settings
from app.db.session import init_db
from app.models.auth_model import AuthModel
from app.routers.download_router import download_router
from app.routers.files_router import files_router
from app.routers.login_router import login_router
from app.routers.logout_router import logout_router
from app.routers.upload_router import upload_router
from app.utils.create_admin_user import create_admin_user

UPLOAD_DIR = Path("uploads/")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

CHUNKS_DIR = UPLOAD_DIR / "chunks"
COMPLETED_DIR = UPLOAD_DIR / "completed"
CHUNK_TTL = timedelta(days=7)
CLEANUP_INTERVAL = 60 * 60


async def main():
    app = Quart(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["QUART_AUTH_COOKIE_SECURE"] = not settings.DEBUG
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_CONTENT_LENGTH

    csrf = CSRFProtect()
    csrf.init_app(app)

    app.asgi_app = ProxyFixMiddleware(
        app.asgi_app,
        mode="legacy",
        trusted_hops=1,
    )

    await init_db()
    await create_admin_user()

    auth_manager = QuartAuth()
    auth_manager.user_class = AuthModel
    auth_manager.init_app(app)

    register_app_blueprints(app)
    make_context(app)
    before_serving_init(app)

    await app.run_task(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.DEBUG,
    )


def before_serving_init(app):
    @app.before_serving
    async def prepare_upload_dirs():
        CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
        COMPLETED_DIR.mkdir(parents=True, exist_ok=True)

    @app.before_serving
    async def start_background():
        await cleanup_old_chunks_once()
        app.add_background_task(chunk_cleanup_loop)


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
    app.register_blueprint(download_router, url_prefix=settings.PREFIX)


if __name__ == "__main__":
    asyncio.run(main())
