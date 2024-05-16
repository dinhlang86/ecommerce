from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

SQLMODEL_DATABASE_URL = (
    "postgresql+asyncpg://postgres:dinhlang@localhost/EcommerceApplicationDatabase"
)

async_engine = create_async_engine(SQLMODEL_DATABASE_URL, echo=True)


# Get asynchroneous session for database
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
