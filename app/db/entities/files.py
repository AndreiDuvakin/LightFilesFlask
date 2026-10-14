from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.entities.base import RootTable


class File(RootTable):
    __tablename__ = "files"

    filename: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
