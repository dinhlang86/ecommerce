from fastapi import HTTPException
from sqlalchemy.engine import ScalarResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.models import User
from app.schemas.user_schema import CreateUserRequest, PutUserPassword
from app.utils.auth_utils import bcrypt_context


async def get_all_users(db: AsyncSession) -> list[User]:
    result: ScalarResult[User] = await db.exec(select(User))
    return list(result.all())


async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    result: User | None = await db.get(User, user_id)
    return result


async def create_new_user(create_user_request: CreateUserRequest, db: AsyncSession) -> None:
    create_user_model = User(
        email=create_user_request.email,
        name=create_user_request.name,
        password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
    )
    db.add(create_user_model)
    await db.commit()


async def update_password(user_view: PutUserPassword, user_id: int, db: AsyncSession) -> None:
    user_model: User | None = await db.get(User, user_id)
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not bcrypt_context.verify(user_view.password, user_model.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    user_model.password = bcrypt_context.hash(user_view.new_password)
    await db.commit()
