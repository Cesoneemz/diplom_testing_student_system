import secrets
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timezone


class Role(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class Token(SQLModel, table=True):
    id: str = Field(default_factory=lambda: secrets.token_urlsafe(32), primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None

    user: Optional["User"] = Relationship(back_populates="tokens")

    expires_at: Optional[datetime] = None

    user: Optional["User"] = Relationship(back_populates="tokens")


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    password_hash: str
    role: Role = Role.student

    tests: List["Test"] = Relationship(back_populates="author")
    results: List["Result"] = Relationship(back_populates="student")
    tokens: list["Token"] = Relationship(back_populates="user")


class Test(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    author_id: UUID = Field(foreign_key="user.id")
    author: Optional[User] = Relationship(back_populates="tests")
    questions: List["Question"] = Relationship(back_populates="test")


class Question(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    test_id: UUID = Field(foreign_key="test.id")
    text: str

    test: Optional[Test] = Relationship(back_populates="questions")
    answers: List["Answer"] = Relationship(back_populates="question")


class Answer(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    question_id: UUID = Field(foreign_key="question.id")
    text: str
    is_correct: bool = False

    question: Optional[Question] = Relationship(back_populates="answers")


class Result(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    student_id: UUID = Field(foreign_key="user.id")
    test_id: UUID = Field(foreign_key="test.id")
    score: int

    student: Optional[User] = Relationship(back_populates="results")
