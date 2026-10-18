from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.entities.users import User
from app.models.user_model import UserModel
from app.repositories.users_repository import UsersRepository


class UsersService:
    def __init__(self, db: AsyncSession):
        self.users_repository = UsersRepository(db)

    async def get_all(self) -> List[UserModel]:
        users = await self.users_repository.get_all()

        return [UserModel.from_entity(user) for user in users]

    async def get_user_by_username(self, username: str) -> UserModel | None:
        user = await self.users_repository.get_by_username(username)

        if not user:
            return None

        return UserModel.from_entity(user)

    async def get_by_id(self, user_id: int) -> UserModel | None:
        user = await self.users_repository.get_by_id(user_id)

        if not user:
            return None

        return UserModel.from_entity(user)

    async def create_user(self, user: UserModel) -> UserModel | None:
        check_user = await self.users_repository.get_by_username(user.username)

        if check_user:
            return None

        new_user = User(
            username=user.username,
        )
        new_user.set_password(user.password)

        new_user = await self.users_repository.create(new_user)

        return UserModel.from_entity(new_user)

    async def check_login(
            self,
            username: str,
            password: str,
    ) -> UserModel | None:
        user = await self.users_repository.get_by_username(username)

        if not user:
            return None

        if user.check_password(password):
            return UserModel.from_entity(user)

        return None
