from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from datetime import datetime
from uuid import UUID
from typing import Annotated

from app.database import db_helper
from app.schemas import UserCreate, UserRead
from app.services.auth import authenticate_user, create_token_for_user
from app.models import Token, User, Role
from app.services.auth import hash_password
from app.dependencies.auth import require_admin
from app.utils import generate_username

from app.security import oauth2_scheme


router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register_user(
    user_data: UserCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(db_helper.session_getter),
    _: User = Depends(require_admin),
):

    if user_data.role == Role.admin:
        raise HTTPException(status_code=403, detail="Нельзя зарегестрировать администратора")

    username = generate_username(user_data.first_name, user_data.middle_name, user_data.last_name)

    stmt = select(User).where((User.email == user_data.email) | (User.username == username))
    result = await session.execute(statement=stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = User(
        email=user_data.email,
        username=username,
        first_name=user_data.first_name,
        middle_name=user_data.middle_name,
        last_name=user_data.last_name,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db_helper.session_getter)):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверные учётные данные")

    token = await create_token_for_user(session, user)
    return {"access_token": str(token.id), "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def read_current_user(request: Request, token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(db_helper.session_getter)):
    stmt = select(Token).where(Token.id == token)
    result = await session.execute(stmt)
    token = result.scalar_one_or_none()
    if not token or (token.expires_at and token.expires_at < datetime.utcnow()):
        raise HTTPException(status_code=401, detail="Недействительный или просроченный токен")

    await session.refresh(token, attribute_names=["user"])
    return token.user

@router.post("/logout")
async def logout(request: Request, session: AsyncSession = Depends(db_helper.session_getter)):
    token_id = request.headers.get("Authorization")
    if not token_id:
        raise HTTPException(status_code=401, detail="Требуется токен")

    try:
        token_uuid = UUID(token_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат токена")

    stmt = select(Token).where(Token.id == token_uuid)
    result = await session.execute(stmt)
    token = result.scalar_one_or_none()
    if not token:
        raise HTTPException(status_code=401, detail="Токен не найден")

    await session.delete(token)
    await session.commit()

    return {"detail": "Выход выполнен успешно"}
