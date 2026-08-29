from question_model import Question


class QuizBrain:
    """Manages quiz progress, user interaction, scoring, and answer validation."""

    def __init__(self, q_list: list[Question]):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list

    def still_has_questions(self) -> bool:
        """Returns True if there are remaining questions in the bank, False otherwise."""
        return self.question_number < len(self.question_list)

    def next_question(self) -> None:
        """Retrieves current question, prompts user for input, and checks the answer."""
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        
        print(f"\nQ.{self.question_number}: [{current_question.category}] ({current_question.difficulty.upper()})")
        print(f"👉 {current_question.text}")

        while True:
            user_answer = input("   Your Answer (True/False or T/F): ").strip().lower()
            if user_answer in ["true", "t"]:
                user_answer = "True"
                break
            elif user_answer in ["false", "f"]:
                user_answer = "False"
                break
            else:
                print("   ⚠️ Invalid input! Please enter 'True' or 'False' (or 't'/'f').")

        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer: str, correct_answer: str) -> None:
        """Compares user answer against correct answer and updates score state."""
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print("✅ That's correct!")
        else:
            print("❌ Oops! That's wrong.")
            print(f"   The correct answer was: {correct_answer}")
        
        print(f"📊 Current Score: {self.score}/{self.question_number}\n" + "─" * 45)

    def get_summary(self) -> str:
        """Returns final score metrics and feedback percentage."""
        total = len(self.question_list)
        percentage = (self.score / total) * 100 if total > 0 else 0
        return f"{self.score}/{total} ({percentage:.1f}%)"
