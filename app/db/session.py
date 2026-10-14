from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import get_db_url
from app.db.entities import Base

engine = create_async_engine(get_db_url(), echo=False)

async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_db():
    async with async_session_maker() as session:
        yield session
