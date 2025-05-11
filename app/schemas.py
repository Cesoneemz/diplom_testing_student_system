from typing import Optional, List
from uuid import UUID
from enum import Enum
from sqlmodel import SQLModel
from pydantic import EmailStr, BaseModel, field_validator


# -------------------------
# ENUM'ы
# -------------------------

class Role(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


# -------------------------
# USER
# -------------------------

class UserBase(SQLModel):
    email: EmailStr
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    role: Role = Role.student

    @field_validator("first_name", "middle_name", "last_name", mode="before")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        """Приводим имя, отчество и фамилию к правильному формату"""
        if value is None:
            return None
        return value.strip().capitalize()


class UserCreate(UserBase):
    password: str  # plain password, будет хэшироваться

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """Валидация пароля"""
        if len(password) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        return password


class UserRead(UserBase):
    id: UUID


# -------------------------
# TEST
# -------------------------

class TestBase(SQLModel):
    title: str


class TestCreate(TestBase):
    pass


class TestRead(TestBase):
    id: UUID
    author_id: UUID


class TestUpdate(SQLModel):
    title: Optional[str] = None


class TestReadFull(TestRead):
    questions: List["QuestionRead"]


# -------------------------
# QUESTION
# -------------------------

class QuestionBase(SQLModel):
    text: str
    test_id: UUID


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: UUID
    answers: List["AnswerRead"]


class QuestionUpdate(SQLModel):
    text: Optional[str] = None


# -------------------------
# ANSWER
# -------------------------

class AnswerBase(SQLModel):
    question_id: UUID
    text: str
    is_correct: bool = False


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    id: UUID


# -------------------------
# RESULT
# -------------------------

class ResultBase(SQLModel):
    student_id: UUID
    test_id: UUID
    score: int


class ResultCreate(ResultBase):
    pass


class ResultRead(BaseModel):
    id: UUID
    test_id: UUID
    student_id: UUID
    score: int


# -------------------------
# SUBMISSION
# -------------------------

class AnswerSubmission(BaseModel):
    question_id: UUID
    answer_id: UUID

class TestSubmission(BaseModel):
    answers: List[AnswerSubmission]


# -------------------------
# СОЗДАНИЕ ТЕСТА С ВОПРОСАМИ И ОТВЕТАМИ
# -------------------------

class AnswerNestedCreate(BaseModel):
    text: str
    is_correct: bool = False


class QuestionNestedCreate(BaseModel):
    text: str
    answers: List[AnswerNestedCreate]


class TestCreateFull(SQLModel):
    title: str
    questions: List[QuestionNestedCreate]

