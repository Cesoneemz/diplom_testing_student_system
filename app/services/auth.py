from typing import Optional

from datetime import datetime
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from app.models import User, Token
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user and verify_password(password, user.password_hash):
        return user
    return None


async def create_token_for_user(session: AsyncSession, user: User) -> Token:
    token = Token(
        user_id=user.id,
        expires_at=datetime.utcnow() + settings.access_token.expires_delta,
    )
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token
