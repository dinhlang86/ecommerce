from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import config
from app.models.user import User

db_name = f"{config.db_name}_test"
db_connection_str = f"postgresql+asyncpg://{config.db_username}:{config.db_password}@\
{config.db_host}:{config.db_port}/{db_name}"


async def prep_db() -> None:
    engine: AsyncEngine = create_async_engine(
        f"""postgresql+asyncpg://postgres:{config.db_password}@{config.db_host}:{config.db_port}
            /postgres""",
        isolation_level="AUTOCOMMIT",
    )
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        await conn.execute(text(f"CREATE DATABASE {db_name}"))


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    await prep_db()
    engine = create_async_engine(
        db_connection_str,
        isolation_level="AUTOCOMMIT",
    )
    session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with session() as s:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield s

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def admin_user(async_session: AsyncSession) -> AsyncGenerator[User, None]:
    user = User(
        id=1,
        email="admin@gmail.com",
        name="admin",
        password="admin",
        role="admin",
    )
    async_session.add(user)
    await async_session.commit()
    yield user
