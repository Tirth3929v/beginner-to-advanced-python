"""
Day 34 - Question Data Model
"""


class Question:
    """Represents a single quiz question with text and boolean answer."""

    def __init__(self, text: str, answer: str):
        self.text = text
        self.answer = answer

    def __repr__(self):
        return f"Question({self.text[:30]}... -> {self.answer})"
