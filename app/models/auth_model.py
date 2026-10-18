from quart_auth import AuthUser

from app.db.session import get_db
from app.services.users_service import UsersService
from app.models.user_model import UserModel


class AuthModel(AuthUser):
    def __init__(self, auth_id: str):
        super().__init__(auth_id)
        self._resolved = False
        self._user: UserModel | None = None

    async def _resolve(self) -> None:
        if not self._resolved:
            async with get_db() as db:
                users_service = UsersService(db)
                self._user = await users_service.get_by_id(int(self.auth_id))
            self._resolved = True

    @property
    async def user(self) -> UserModel | None:
        await self._resolve()
        return self._user
