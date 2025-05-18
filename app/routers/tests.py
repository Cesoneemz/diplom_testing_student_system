from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

from app.database import db_helper
from app.models import Test, User, Answer, Question, Result, Role
from app.schemas import (
    TestCreateFull,
    TestReadFull,
    TestUpdate,
    QuestionUpdate,
    TestSubmission,
    ResultRead,
)
from app.dependencies.auth import get_current_user, require_admin

router = APIRouter(prefix="/tests", tags=["Tests"])


# ---------------------------
# СОЗДАНИЕ ТЕСТА С ВОПРОСАМИ
# ---------------------------
@router.post("/", response_model=TestReadFull)
async def create_test(
    test_data: TestCreateFull,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [Role.admin, Role.teacher]:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    new_test = Test(title=test_data.title, author_id=current_user.id)
    session.add(new_test)
    await session.commit()
    await session.refresh(new_test)

    for question_data in test_data.questions:
        new_question = Question(text=question_data.text, test_id=new_test.id)
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)

        for answer_data in question_data.answers:
            answer = Answer(
                question_id=new_question.id,
                text=answer_data.text,
                is_correct=answer_data.is_correct,
            )
            session.add(answer)

    await session.commit()

    # Перезапрашиваем тест с вопросами и ответами через eager loading
    statement = (
        select(Test)
        .where(Test.id == new_test.id)
        .options(
            selectinload(Test.questions).selectinload(Question.answers)
        )
    )
    result = await session.execute(statement)
    test_with_relations = result.scalars().first()

    return test_with_relations


# ---------------------------
# СПИСОК ВСЕХ ТЕСТОВ (с вопросами и ответами)
# ---------------------------
@router.get("/", response_model=List[TestReadFull])
async def list_tests(
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
    _ = Depends(require_admin)
):
    result = await session.execute(select(Test).options(
        selectinload(Test.questions).selectinload(Question.answers)
    ))
    tests = result.scalars().all()
    return tests


# ---------------------------
# ОДИН ТЕСТ ПО ID (с вопросами)
# ---------------------------
@router.get("/{test_id}", response_model=TestReadFull)
async def get_test(
    test_id: UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    test = await session.execute(select(Test).options(
        selectinload(Test.questions).selectinload(Question.answers)
    ).where(Test.id == test_id))

    test = test.scalars().first()

    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    return test


# ---------------------------
# ОБНОВЛЕНИЕ ТЕСТА
# ---------------------------
@router.put("/{test_id}", response_model=TestReadFull)
async def update_test(
    test_id: UUID,
    test_data: TestUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    test = await session.get(Test, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    if current_user.role not in [Role.admin, Role.teacher] or test.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    for key, value in test_data.model_dump(exclude_unset=True).items():
        setattr(test, key, value)

    await session.commit()
    await session.refresh(test)
    return test


# ---------------------------
# УДАЛЕНИЕ ТЕСТА + каскадное удаление вопросов и ответов
# ---------------------------
@router.delete("/{test_id}")
async def delete_test(
    test_id: UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    test = await session.get(Test, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    if current_user.role != Role.admin and test.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    stmt = select(Question).where(Question.test_id == test.id)
    result = await session.execute(stmt)
    questions = result.scalars().all()

    for question in questions:
        await session.execute(
            select(Answer).where(Answer.question_id == question.id).delete()
        )
        await session.delete(question)

    await session.delete(test)
    await session.commit()
    return {"ok": True}


# ---------------------------
# ОБНОВЛЕНИЕ ОДНОГО ВОПРОСА
# ---------------------------
@router.put("/questions/{question_id}")
async def update_question(
    question_id: UUID,
    question_data: QuestionUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    question = await session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    test = await session.get(Test, question.test_id)
    if current_user.role not in [Role.admin, Role.teacher] or test.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    for key, value in question_data.model_dump(exclude_unset=True).items():
        setattr(question, key, value)

    await session.commit()
    await session.refresh(question)
    return question


# ---------------------------
# УДАЛЕНИЕ ВОПРОСА + его ответов
# ---------------------------
@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    question = await session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    test = await session.get(Test, question.test_id)
    if current_user.role not in [Role.admin, Role.teacher] or test.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    await session.execute(select(Answer).where(Answer.question_id == question.id).delete())
    await session.delete(question)
    await session.commit()
    return {"ok": True}


# ---------------------------
# СДАЧА ТЕСТА СТУДЕНТОМ
# ---------------------------
@router.post("/{test_id}/submit", response_model=ResultRead)
async def submit_test(
    test_id: UUID,
    submission: TestSubmission,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    # if current_user.role != Role.student:
        # raise HTTPException(status_code=403, detail="Только студент может сдавать тест")

    test = await session.get(Test, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")

    question_ids = [item.question_id for item in submission.answers]
    answer_ids = [item.answer_id for item in submission.answers]

    question_stmt = select(Question).where(Question.id.in_(question_ids))
    question_result = await session.execute(question_stmt)
    questions = question_result.scalars().all()

    answer_stmt = select(Answer).where(Answer.id.in_(answer_ids))
    answer_result = await session.execute(answer_stmt)
    answers = answer_result.scalars().all()

    valid_answer_map = {answer.id: answer for answer in answers}
    correct_count = 0

    for question in questions:
        answer_id = next((item.answer_id for item in submission.answers if item.question_id == question.id), None)
        if answer_id not in valid_answer_map:
            raise HTTPException(status_code=400, detail="Ответ не найден")
        answer = valid_answer_map[answer_id]
        if answer.question_id != question.id:
            raise HTTPException(status_code=400, detail="Ответ не соответствует вопросу")
        if answer.is_correct:
            correct_count += 1

    result = Result(
        student_id=current_user.id,
        test_id=test_id,
        score=correct_count,
    )
    session.add(result)
    await session.commit()
    await session.refresh(result)

    result_read = ResultRead(
        id=result.id,
        student_id=result.student_id,
        test_id=result.test_id,
        score=result.score,
        test_title=None
    )

    return result_read

