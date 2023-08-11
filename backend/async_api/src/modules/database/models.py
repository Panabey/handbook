from datetime import datetime

from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Handbook(Base):
    __tablename__ = "handbook"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[str] = mapped_column(String, nullable=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=False)
    status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("status.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    content: Mapped[list["HandbookContent"]] = relationship(back_populates="hbook")
    status_info: Mapped["Status"] = relationship(back_populates="hbook_status")


class HandbookContent(Base):
    __tablename__ = "handbook_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    handbook_id: Mapped[int] = mapped_column(Integer, ForeignKey("handbook.id"))
    title: Mapped[str] = mapped_column(String(80))
    is_visible: Mapped[bool] = mapped_column(Boolean, default=False)

    hbook: Mapped["Handbook"] = relationship(back_populates="content")
    hbook_page: Mapped[list["HandbookPage"]] = relationship(
        back_populates="hbook_content"
    )


class HandbookPage(Base):
    __tablename__ = "handbook_page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content_id: Mapped[int] = mapped_column(Integer, ForeignKey("handbook_content.id"))
    title: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(Text)
    reading_time: Mapped[int] = mapped_column(Integer)
    update_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    create_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    is_visible: Mapped[bool] = mapped_column(Boolean, default=False)

    hbook_content: Mapped["HandbookContent"] = relationship(back_populates="hbook_page")


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(25))

    hbook_status: Mapped[list[Handbook]] = relationship(
        back_populates="status_info",
        cascade="all, delete",
        passive_deletes=True,
    )


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(80))
    anons: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text)
    update_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    create_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    reading_time: Mapped[int] = mapped_column(Integer)


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String, nullable=True)

    questions_info: Mapped[list["Question"]] = relationship(
        back_populates="quiz_info",
        cascade="all, delete",
        passive_deletes=True,
    )


class Question(Base):
    __tablename__ = "quiz_question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    quiz_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quiz.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(200))
    hint: Mapped[str] = mapped_column(String(200), nullable=True)

    answers_info: Mapped[list["Answer"]] = relationship(
        back_populates="question_info",
        cascade="all, delete",
        passive_deletes=True,
    )
    quiz_info: Mapped["Quiz"] = relationship(back_populates="questions_info")


class Answer(Base):
    __tablename__ = "quiz_answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quiz_question.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(200))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    explanation: Mapped[str] = mapped_column(String(200), nullable=True)

    question_info: Mapped["Question"] = relationship(back_populates="answers_info")
