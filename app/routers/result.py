from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from uuid import UUID

from app.database import db_helper
from app.models import Result, Role, User, Test
from app.schemas import ResultRead
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/results", tags=["Results"])

@router.get("/", response_model=List[ResultRead])
async def list_results(
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    # SQLAlchemy join Result + Test
    stmt = (
        select(
            Result.id,
            Result.score,
            Result.test_id,
            Test.title.label("test_title")
        )
        .join(Test, Result.test_id == Test.id)
    )

    if current_user.role == Role.student:
        stmt = stmt.where(Result.student_id == current_user.id)

    result = await session.execute(stmt)
    rows = result.all()

    # Формируем список словарей для Pydantic
    results_list = []
    results_list = [
        ResultRead(
            id=r.id,
            score=r.score,
            test_id=r.test_id,
            student_id=current_user.id,
            test_title=r.test_title,
        )
        for r in rows
    ]

    print(results_list)

    return results_list

@router.get("/{result_id}", response_model=ResultRead)
async def get_result(
    result_id: UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    result = await session.get(Result, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Результат не найден")

    if current_user.role == Role.student and result.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return result
