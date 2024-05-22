import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User


@pytest.mark.asyncio
async def test_user_creation(admin_user: User, async_session: AsyncSession) -> None:
    admin: User | None = await async_session.get(User, admin_user.id)
    assert admin is not None
    assert admin.email == admin_user.email
    assert admin.name == admin_user.name


@pytest.mark.asyncio
async def test_get_all_users(admin_user: User, admin_token: str, client: AsyncClient) -> None:
    # Test invalid token
    # response = await client.get(
    #     "/user",
    #     headers={"Authorization": "Bearer dsafdfasdjl"},
    # )
    # assert response.status_code == 401
    # Test valid token
    response = await client.get(
        "/user",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["email"] == admin_user.email
    assert users[0]["name"] == admin_user.name
