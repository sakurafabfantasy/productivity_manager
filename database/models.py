from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key = True)
    title = mapped_column(String(100))
    content =  mapped_column(String(100))
    tag: Mapped[str | None] = mapped_column(String(50), default = None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title = mapped_column(String(100))
    is_completed: Mapped[bool] = mapped_column()
    tag: Mapped[str | None] = mapped_column(String(50), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    expiring_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Flashcards(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(100))
    trword: Mapped[str] = mapped_column(String(100))
    language: Mapped[str] = mapped_column(String(100))
    status: Mapped[int] = mapped_column(default=0)
    available_after: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


