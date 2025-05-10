from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.database import db_helper
from app.models import Test, User, Role
from app.schemas import TestCreate, TestRead, TestUpdate
from app.dependencies.auth import get_current_user
from typing import List

router = APIRouter(prefix="/tests", tags=["Tests"])

@router.post("/", response_model=TestRead)
async def create_test(
    test_data: TestCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [Role.admin, Role.teacher]:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    new_test = Test(**test_data.dict(), author_id=current_user.id)
    session.add(new_test)
    await session.commit()
    await session.refresh(new_test)
    return new_test

@router.get("/", response_model=List[TestRead])
async def list_tests(
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(select(Test))
    return result.scalars().all()

@router.get("/{test_id}", response_model=TestRead)
async def get_test(
    test_id: UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    test = await session.get(Test, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    return test

@router.put("/{test_id}", response_model=TestRead)
async def update_test(
    test_id: UUID,
    test_data: TestUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user)
):
    test = await session.get(Test, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    if current_user.role not in [Role.admin, Role.teacher] or test.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    for key, value in test_data.dict(exclude_unset=True).items():
        setattr(test, key, value)

    await session.commit()
    await session.refresh(test)
    return test

@router.delete("/{test_id}")
async def delete_test(
    test_id: UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user)
):
    test = await session.get(Test, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    if current_user.role != Role.admin and test.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    await session.delete(test)
    await session.commit()
    return {"ok": True}
