from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata_obj = MetaData()


class Base(DeclarativeBase):
    metadata = metadata_obj


from app.db.entities.files import File  # noqa: E402
from app.db.entities.users import User  # noqa: E402
