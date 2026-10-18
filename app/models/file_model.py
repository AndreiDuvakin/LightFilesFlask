from dataclasses import dataclass, field
import datetime

from app.db.entities.files import File


@dataclass
class FileModel:
    filename: str
    uploaded_at: datetime.datetime
    size: int
    id: int | None = field(default=None)

    @classmethod
    def from_entity(cls, file: File):
        return cls(
            id=file.id,
            filename=file.filename,
            uploaded_at=file.uploaded_at,
            size=file.size,
        )

    def to_entity(self):
        file = File(
            filename=self.filename,
            uploaded_at=self.uploaded_at,
            size=self.size,
        )

        if self.id is not None:
            file.id = self.id

        return file

    @property
    def format_size(self) -> str:
        if self.size < 1024:
            return f"{self.size} Б"

        if self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} КБ"

        if self.size < 1024 * 1024 * 1024:
            return f"{self.size / 1024 / 1024:.1f} MБ"

        return f"{self.size / 1024 / 1024 / 1024:.1f} ГБ"

    @property
    def pretty_uploaded_at(self) -> str:
        return self.uploaded_at.strftime("%d.%m.%Y %H:%M:%S")
