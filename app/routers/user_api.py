from fastapi import APIRouter, Depends
from starlette import status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_async_session
from app.models import User
from app.services.user_service import get_all_users
from app.schemas.user_schema import CreateUserRequest
from app.services.user_service import create_new_user


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/list", status_code=status.HTTP_200_OK)
async def get_user(*, session: AsyncSession = Depends(get_async_session)) -> list[User]:
    users: list[User] = await get_all_users(session)
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest, db: AsyncSession = Depends(get_async_session)
) -> None:
    await create_new_user(create_user_request, db)
