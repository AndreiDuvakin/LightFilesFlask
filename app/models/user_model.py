from dataclasses import dataclass, field

from app.db.entities.users import User


@dataclass
class UserModel:
    username: str
    password: str
    id: int | None = field(default=None)

    @classmethod
    def from_entity(cls, user: User):
        return cls(username=user.username, password=user.password_hash)

    def to_entity(self):
        user = User(username=self.username, password_hash=self.password)

        if self.id is not None:
            user.id = self.id

        return user
