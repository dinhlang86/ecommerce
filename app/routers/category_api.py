from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.core.database import get_async_session
from app.models.category import Category, CategoryCreate, CategoryPublic, CategoryUpdate
from app.models.user import TokenUser
from app.services.auth_service import get_admin_user, get_current_user
from app.services.category_service import (
    create_new_category,
    delete_category_by_id,
    get_all_categories,
    get_category_by_id,
    update_category_info,
)

router = APIRouter(prefix="/category", tags=["category"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_categories(
    _: TokenUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[Category]:
    categories: list[Category] = await get_all_categories(session)
    return categories


@router.get(
    "/category/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryPublic
)
async def get_category_id(
    category_id: int,
    _: TokenUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Category:
    category: Category | None = await get_category_by_id(category_id, session)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryPublic)
async def create_category(
    category_request: CategoryCreate,
    _: TokenUser = Depends(get_admin_user),
    db: AsyncSession = Depends(get_async_session),
) -> Category:
    category: Category = await create_new_category(category_request, db)
    return category


@router.put("/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_category(
    category_view: CategoryUpdate,
    category_id: int,
    _: TokenUser = Depends(get_admin_user),
    db: AsyncSession = Depends(get_async_session),
) -> None:
    await update_category_info(category_view, category_id, db)


@router.delete("/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    _: TokenUser = Depends(get_admin_user),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await delete_category_by_id(category_id, session)
