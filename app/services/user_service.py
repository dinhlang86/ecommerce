from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import User
from sqlmodel import select
from sqlalchemy.engine import ScalarResult
from app.schemas.user_schema import CreateUserRequest
from app.utils.auth_utils import bcrypt_context


async def get_all_users(db: AsyncSession) -> list[User]:
    result: ScalarResult[User] = await db.exec(select(User))
    return list(result.all())


async def create_new_user(create_user_request: CreateUserRequest, db: AsyncSession) -> None:
    create_user_model = User(
        email=create_user_request.email,
        name=create_user_request.name,
        password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
    )
    db.add(create_user_model)
    await db.commit()
