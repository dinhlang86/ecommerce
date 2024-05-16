from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.core.database import get_async_session
from app.models import User
from app.models.user import TokenUser
from app.schemas.user_schema import CreateUserRequest
from app.services.auth_service import get_admin_user
from app.services.user_service import create_new_user, get_all_users, get_user_by_id

router = APIRouter(prefix="/user", tags=["user"])


# Get all users in the database, only admin can access this API
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(
    _: TokenUser = Depends(get_admin_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[User]:
    users: list[User] = await get_all_users(session)
    return users


# Get user by id, only admin can access this API
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_id(
    _: TokenUser = Depends(get_admin_user),
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Path(gt=0),
) -> User:
    user: User | None = await get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# Create a new user in the database, only admin can access this API
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest,
    _: TokenUser = Depends(get_admin_user),
    db: AsyncSession = Depends(get_async_session),
) -> None:
    await create_new_user(create_user_request, db)
