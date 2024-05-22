import asyncio
from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import config
from app.core.database import db_connection_str
from app.models.user import User

db_name = f"{config.db_name}_test"
test_db_connection_str = f"postgresql+asyncpg://{config.db_username}:{config.db_password}@\
{config.db_host}:{config.db_port}/{db_name}"


@pytest.fixture(scope="session")
def event_loop(request: Any) -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db(event_loop: asyncio.AbstractEventLoop) -> AsyncGenerator[None, None]:
    assert test_db_connection_str != db_connection_str
    engine: AsyncEngine = create_async_engine(
        f"""postgresql+asyncpg://postgres:{config.db_password}@{config.db_host}:{config.db_port}
            /postgres""",
        isolation_level="AUTOCOMMIT",
    )
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        await conn.execute(text(f"CREATE DATABASE {db_name}"))
    yield
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(test_db: Any) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        test_db_connection_str,
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
