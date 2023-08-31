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
    title: Mapped[str] = mapped_column(String(80), unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[str] = mapped_column(String, nullable=True)
    status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("status.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    content: Mapped[list["HandbookContent"]] = relationship(
        back_populates="hbook",
        cascade="all, delete",
        passive_deletes=True,
    )
    status_info: Mapped["Status"] = relationship(back_populates="hbook_status")


class HandbookContent(Base):
    __tablename__ = "handbook_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    handbook_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("handbook.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(255))

    hbook: Mapped["Handbook"] = relationship(back_populates="content")
    hbook_page: Mapped[list["HandbookPage"]] = relationship(
        back_populates="hbook_content", cascade="all, delete", passive_deletes=True
    )


class HandbookPage(Base):
    __tablename__ = "handbook_page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("handbook_content.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    title: Mapped[str] = mapped_column(String(80))
    short_description: Mapped[str] = mapped_column(String(160))
    text: Mapped[str] = mapped_column(Text)
    reading_time: Mapped[int] = mapped_column(Integer)
    update_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    create_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    hbook_content: Mapped["HandbookContent"] = relationship(back_populates="hbook_page")


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(25), unique=True)

    hbook_status: Mapped[list[Handbook]] = relationship(
        back_populates="status_info",
        cascade="all, delete",
        passive_deletes=True,
    )


class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    logo_url: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String(80))
    anons: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text)
    update_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    create_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    reading_time: Mapped[int] = mapped_column(Integer)

    tags_article_info: Mapped[list["Tag"]] = relationship(
        secondary="article_tag", back_populates="articles_tag"
    )


class ArticleTag(Base):
    __tablename__ = "article_tag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("article.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tag.id", ondelete="CASCADE", onupdate="CASCADE")
    )


class QuizTag(Base):
    __tablename__ = "quiz_tag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quiz.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tag.id", ondelete="CASCADE", onupdate="CASCADE")
    )


class TagStatus(Base):
    __tablename__ = "tag_status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(60), unique=True)

    tag_info: Mapped[list["Tag"]] = relationship(
        back_populates="status_info",
        cascade="all, delete",
        passive_deletes=True,
    )


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(60), unique=True)
    status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tag_status.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )

    status_info: Mapped[TagStatus] = relationship(back_populates="tag_info")
    quizzez_tag: Mapped[list["Quiz"]] = relationship(
        secondary="quiz_tag", back_populates="tags_quiz_info"
    )
    articles_tag: Mapped[list["Article"]] = relationship(
        secondary="article_tag", back_populates="tags_article_info"
    )


class QuizTopic(Base):
    __tablename__ = "quiz_topic"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(60), unique=True)

    quizzes_info: Mapped[list["Quiz"]] = relationship(
        back_populates="topic_info",
        cascade="all, delete",
        passive_deletes=True,
    )


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    topic_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("quiz_topic.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    logo_url: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String(100))
    short_description: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(String(255))

    topic_info: Mapped[QuizTopic] = relationship(back_populates="quizzes_info")
    questions_info: Mapped[list["Question"]] = relationship(
        back_populates="quiz_info",
        cascade="all, delete",
        passive_deletes=True,
    )
    tags_quiz_info: Mapped[list["Tag"]] = relationship(
        secondary="quiz_tag", back_populates="quizzez_tag"
    )


class Question(Base):
    __tablename__ = "quiz_question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    quiz_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quiz.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    text: Mapped[str] = mapped_column(String(255))
    hint: Mapped[str] = mapped_column(String(255), nullable=True)

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
    text: Mapped[str] = mapped_column(String(255))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    explanation: Mapped[str] = mapped_column(String(255), nullable=True)

    question_info: Mapped["Question"] = relationship(back_populates="answers_info")
