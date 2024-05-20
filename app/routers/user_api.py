from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.core.database import get_async_session
from app.models.user import DisplayUser, TokenUser, User
from app.schemas.user_schema import CreateUserRequest, PutUserPassword
from app.services.auth_service import check_admin_or_current_user, get_admin_user
from app.services.user_service import (
    create_new_user,
    delete_user_by_id,
    get_all_users,
    get_user_by_id,
    update_password,
)

router = APIRouter(prefix="/user", tags=["user"])


# Get all users in the database, only admin can access this API
@router.get("", status_code=status.HTTP_200_OK)
async def get_user(
    _: TokenUser = Depends(get_admin_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[DisplayUser]:
    users: list[User] = await get_all_users(session)
    return [DisplayUser.model_validate(user) for user in users]


# Get user by id, only admin can access this API
@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_id(
    _: TokenUser = Depends(get_admin_user),
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Path(gt=0),
) -> DisplayUser:
    user: User | None = await get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return DisplayUser.model_validate(user)


# Create a new user in the database, only admin can access this API
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest,
    _: TokenUser = Depends(get_admin_user),
    db: AsyncSession = Depends(get_async_session),
) -> None:
    await create_new_user(create_user_request, db)


# Admin can change password for admin or user
@router.put("/password/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user_view: PutUserPassword,
    user_id: int,
    _: TokenUser = Depends(check_admin_or_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> None:
    await update_password(user_view, user_id, db)


# Admin can delete user based on id
@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    _: TokenUser = Depends(get_admin_user),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await delete_user_by_id(user_id, session)
