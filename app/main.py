import asyncio

from flask import Flask

from app.core.settings import settings
from app.db.session import init_db


async def main():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    await init_db()
    run_app(app)


def run_app(app):
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.DEBUG)


if __name__ == '__main__':
    asyncio.run(main())
