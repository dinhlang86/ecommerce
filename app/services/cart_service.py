from sqlalchemy.engine import ScalarResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.cart import Cart, CartCreate
from app.models.user import Role, TokenUser


async def create_new_cart(cart_request: CartCreate, db: AsyncSession, user_id: int) -> Cart:
    cart = Cart(**cart_request.model_dump())
    cart.user_id = user_id
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    return cart


async def get_carts(db: AsyncSession, user: TokenUser) -> list[Cart] | None:
    result: ScalarResult[Cart] | None = None
    if user.role == Role.admin:
        result = await db.exec(select(Cart))
    else:
        result = await db.exec(select(Cart).where(Cart.user_id == user.id))
    return list(result.all())


async def get_cart_by_id(cart_id: int, db: AsyncSession, user: TokenUser) -> Cart | None:
    result: ScalarResult[Cart] | None = None
    if user.role == Role.admin:
        result = await db.exec(select(Cart).where(Cart.id == cart_id))
    else:
        result = await db.exec(
            select(Cart).where(Cart.id == cart_id).where(Cart.user_id == user.id)
        )
    return result.first()
