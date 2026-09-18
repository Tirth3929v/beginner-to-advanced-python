"""
Day 34 - Quiz Brain Controller
Manages question sequence, score computation, and answer validation.
"""

import html


class QuizBrain:
    """Core game engine managing question advancement and score tracking."""

    def __init__(self, q_list: list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self) -> bool:
        """Returns True if there are remaining questions in the list."""
        return self.question_number < len(self.question_list)

    def next_question(self) -> str:
        """Retrieves next question, unescapes HTML entities, and increments pointer."""
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer: str) -> bool:
        """Validates user's answer against correct answer (case-insensitive)."""
        correct_answer = self.current_question.answer
        if user_answer.strip().lower() == correct_answer.strip().lower():
            self.score += 1
            return True
        return False
