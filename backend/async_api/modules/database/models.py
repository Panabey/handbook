from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    content_info: Mapped[list["CourseContent"]] = relationship(
        back_populates="course_info"
    )


class CourseContent(Base):
    __tablename__ = "course_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("course.id"))
    title: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(String)
    reading_time: Mapped[int] = mapped_column(Integer)
    update_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    create_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    course_info: Mapped["Course"] = relationship(
        back_populates="content_info"
    )
