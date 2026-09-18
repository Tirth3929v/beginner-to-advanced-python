import sys
from art import logo, trophy_art
from data import question_data
from question_model import Question
from quiz_brain import QuizBrain

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution function for the OOP Quiz Game."""
    print(logo)
    print("Welcome to the Ultimate OOP Python & CS Trivia Challenge! 🎯\n")

    # Build question bank from raw data using Question objects
    question_bank: list[Question] = []
    for q in question_data:
        q_text = q["question"]
        q_answer = q["correct_answer"]
        q_cat = q.get("category", "General")
        q_diff = q.get("difficulty", "Medium")
        new_question = Question(q_text, q_answer, q_cat, q_diff)
        question_bank.append(new_question)

    # Initialize QuizBrain object instance
    quiz = QuizBrain(question_bank)

    # Main Quiz Loop
    while quiz.still_has_questions():
        quiz.next_question()

    # Final Results & Performance Summary
    print("\n" + "═" * 50)
    print("      🎉 CONGRATULATIONS! YOU HAVE COMPLETED THE QUIZ 🎉")
    print("═" * 50)
    print(trophy_art)
    print(f"🏆 Final Score: {quiz.get_summary()}")
    
    score_ratio = quiz.score / len(question_bank) if question_bank else 0
    if score_ratio == 1.0:
        print("🌟 PERFECT SCORE! You are a master Python & CS engineer! 🚀\n")
    elif score_ratio >= 0.7:
        print("👏 Great job! Excellent understanding of key concepts. Keep it up! 💪\n")
    else:
        print("📚 Good effort! Keep practicing to master OOP and CS fundamentals! 🐍\n")


if __name__ == "__main__":
    main()
