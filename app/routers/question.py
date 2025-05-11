from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.database import db_helper
from app.models import Question, Test, User
from app.schemas import QuestionCreate, QuestionRead, QuestionUpdate
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=QuestionRead)
async def create_question(
    question: QuestionCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Test).where(Test.id == question.test_id)
    result = await session.execute(stmt)
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    if test.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав для добавления вопроса")

    new_question = Question(text=question.text, test_id=question.test_id)
    session.add(new_question)
    await session.commit()
    await session.refresh(new_question)
    return new_question


@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(
    question_id: UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(Question).where(Question.id == question_id)
    result = await session.execute(stmt)
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    return question


@router.patch("/{question_id}", response_model=QuestionRead)
async def update_question(
    question_id: UUID,
    question_update: QuestionUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Question)
        .where(Question.id == question_id)
        .join(Test)
        .where(Test.author_id == current_user.id)
    )
    result = await session.execute(stmt)
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден или нет доступа")

    if question_update.text is not None:
        question.text = question_update.text

    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Question)
        .where(Question.id == question_id)
        .join(Test)
        .where(Test.author_id == current_user.id)
    )
    result = await session.execute(stmt)
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден или нет доступа")

    await session.delete(question)
    await session.commit()
