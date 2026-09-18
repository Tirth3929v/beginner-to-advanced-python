"""
Day 66: Cafe Model & Serialization Architecture
Implements SQLAlchemy ORM entity with automatic dictionary serialization for JSON responses.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from typing import Dict, Any


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Cafe(db.Model):
    __tablename__ = "cafe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """Converts model instance to JSON-serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "map_url": self.map_url,
            "img_url": self.img_url,
            "location": self.location,
            "seats": self.seats,
            "has_toilet": self.has_toilet,
            "has_wifi": self.has_wifi,
            "has_sockets": self.has_sockets,
            "can_take_calls": self.can_take_calls,
            "coffee_price": self.coffee_price,
        }
