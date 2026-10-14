from dataclasses import dataclass, field
import datetime

from app.db.entities.files import File


@dataclass
class FileModel:
    filename: str
    uploaded_at: datetime.datetime
    size: int
    id: int | None = field(default=None)
    upload_progress: float | None = field(default=None)

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
            filename=self.filename, uploaded_at=self.uploaded_at, size=self.size
        )

        if self.id is not None:
            file.id = self.id

        return file
