"""
Day 88: Todo Task Database Model
SQLAlchemy 2.0 ORM schema for tasks with priorities and categories.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Task(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="General")
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="Medium")
    due_date: Mapped[str] = mapped_column(String(50), nullable=False, default="Today")
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[str] = mapped_column(String(50), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "priority": self.priority,
            "due_date": self.due_date,
            "is_completed": self.is_completed,
            "created_at": self.created_at
        }
