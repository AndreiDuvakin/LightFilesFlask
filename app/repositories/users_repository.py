from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.entities.users import User


class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[User]:
        query = select(User)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).filter_by(username=username)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, user: User) -> User | None:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
