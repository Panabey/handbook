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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    content_info: Mapped[list["HandbookContent"]] = relationship(
        back_populates="handbook_info"
    )


class HandbookContent(Base):
    __tablename__ = "handbook_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("handbook.id"))
    title: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(String)
    reading_time: Mapped[int] = mapped_column(Integer)
    update_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    create_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    handbook_info: Mapped["Handbook"] = relationship(back_populates="handbook_info")
