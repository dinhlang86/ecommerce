from app.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import ALGORITHM, SECRET_KEY
from app.utils.auth_utils import bcrypt_context
from sqlmodel import select


async def authenticate_user(email: str, password: str, db: AsyncSession) -> User | None:
    result = await db.exec(select(User).where(User.email == email))
    user = result.first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.password):
        return None
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str:
    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
