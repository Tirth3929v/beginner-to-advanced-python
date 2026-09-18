"""
Day 68: User Authentication Model Definitions
Integrates Flask-Login UserMixin with modern SQLAlchemy 2.0 ORM.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)

    def __repr__(self) -> str:
        return f"<User #{self.id}: {self.email} ({self.name})>"
