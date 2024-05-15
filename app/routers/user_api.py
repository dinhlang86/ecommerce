from fastapi import APIRouter, Depends
from starlette import status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_async_session
from app.models import User
from app.services.user_service import get_all_users

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(*, session: AsyncSession = Depends(get_async_session)) -> list[User]:
    users: list[User] = await get_all_users(session)
    return users
