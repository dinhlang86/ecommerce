from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import User
from sqlmodel import select
from sqlalchemy.engine import ScalarResult


async def get_all_users(db: AsyncSession) -> list[User]:
    result: ScalarResult[User] = await db.exec(select(User))
    return list(result.all())
