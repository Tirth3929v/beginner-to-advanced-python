"""
Day 57: Blog Post Data Model
OOP model wrapping individual blog article attributes.
"""

from typing import Dict, Any


class Post:
    def __init__(self, post_id: int, title: str, subtitle: str, body: str, author: str = "Tirth Patel", date: str = "September 2026"):
        self.id = post_id
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.author = author
        self.date = date

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Post":
        return cls(
            post_id=data.get("id", 0),
            title=data.get("title", "Untitled"),
            subtitle=data.get("subtitle", ""),
            body=data.get("body", ""),
            author=data.get("author", "Tirth Patel"),
            date=data.get("date", "September 2026"),
        )
