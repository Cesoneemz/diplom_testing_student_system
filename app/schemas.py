from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel
from enum import Enum
from pydantic import validator, EmailStr


class Role(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class UserBase(SQLModel):
    email: EmailStr
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    role: Role = Role.student

    @validator("first_name", "middle_name", "last_name")
    def validate_name(cls, value: str) -> str:
        """Приводим имя, отчество и фамилию к правильному формату"""
        if value is None:
            return None
        return value.strip().capitalize()


class UserCreate(UserBase):
    password: str  # plain password, будет хэшироваться

    @validator("password")
    def validate_password(cls, password: str) -> str:
        """Валидация пароля"""
        if len(password) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        return password


class UserRead(UserBase):
    id: UUID  # используем UUID вместо int


class TestBase(SQLModel):
    title: str


class TestCreate(TestBase):
    pass  # author_id будет устанавливаться из авторизованного пользователя


class TestRead(TestBase):
    id: UUID
    author_id: UUID


class TestUpdate(SQLModel):
    title: Optional[str] = None


class QuestionBase(SQLModel):
    text: str
    test_id: UUID


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: UUID


class QuestionUpdate(SQLModel):
    text: Optional[str] = None