from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from app.models import Role, User, Token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.database import db_helper
from starlette.status import HTTP_401_UNAUTHORIZED

from app.security import oauth2_scheme

async def get_current_user(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    
    stmt = select(Token).where(Token.id == token)
    result = await session.execute(stmt)
    token_pg = result.scalar_one_or_none()

    if token_pg is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="Недействительный токен")

    user_stmt = select(User).where(User.id == token_pg.user_id)
    user_result = await session.execute(user_stmt)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Неавторизован"
        )

    return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ разрешён только администраторам"
        )
    return user
