from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User


async def test_user(admin_user: User, async_session: AsyncSession) -> None:
    admin: User | None = await async_session.get(User, admin_user.id)
    assert admin is not None
    assert admin.email == admin_user.email
    assert admin.name == admin_user.name
