from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    UPLOAD_FOLDER: str
    PREFIX: str = Field(alias="prefix", default="")
    DEBUG: bool = Field(alias="debug", default=False)
    APP_PORT: int = Field(alias="port", default=6767)
    DB_PATH: str = Field(alias="db", default="db.sqlite3")
    APP_HOST: str = Field(alias="host", default="localhost")
    MAX_CONTENT_LENGTH: int = Field(
        alias="max-content-length", default=16 * 1024 * 1024 * 1024
    )

    class Config:
        env_file = ".env"


settings = Settings()


def get_db_url() -> str:
    return f"sqlite+aiosqlite:///{settings.DB_PATH}"
