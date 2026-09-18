class Question:
    """Models a single quiz question with text, answer, category, and difficulty level."""

    def __init__(self, text: str, answer: str, category: str = "General", difficulty: str = "Medium"):
        self.text = text
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def __repr__(self) -> str:
        return f"<Question: {self.text[:30]}... | Ans: {self.answer}>"
