from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

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
    is_visible: Mapped[bool] = mapped_column(default=False)

    content: Mapped[list["HandbookContent"]] = relationship(back_populates="hbook")


class HandbookContent(Base):
    __tablename__ = "handbook_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    handbook_id: Mapped[int] = mapped_column(Integer, ForeignKey("handbook.id"))
    title: Mapped[str] = mapped_column(String(80))
    is_visible: Mapped[bool] = mapped_column(default=False)

    hbook: Mapped["Handbook"] = relationship(back_populates="content")
    hbook_page: Mapped[list["HandbookPage"]] = relationship(
        back_populates="hbook_content"
    )


class HandbookPage(Base):
    __tablename__ = "handbook_page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    handbook_title_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("handbook_content.id")
    )
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    title: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(String)
    reading_time: Mapped[int] = mapped_column(Integer)
    update_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    create_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    is_visible: Mapped[bool] = mapped_column(default=False)

    hbook_content: Mapped["HandbookContent"] = relationship(back_populates="hbook_page")


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(String)
    update_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    create_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    reading_time: Mapped[int] = mapped_column(Integer)
