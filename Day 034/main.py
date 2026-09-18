"""
Day 34 - GUI Quizzer App Studio
Main launcher connecting Open Trivia DB, Question model, QuizBrain, and QuizInterface.
"""

import sys
from art import logo
from data import fetch_quiz_questions
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def build_question_bank() -> list:
    """Fetches trivia questions and constructs a list of Question objects."""
    raw_data = fetch_quiz_questions()
    return [Question(item["question"], item["correct_answer"]) for item in raw_data]


def run_terminal_quiz():
    """Runs the quiz directly in the terminal."""
    questions = build_question_bank()
    quiz = QuizBrain(questions)

    print("\n" + "=" * 65)
    print(" 🧠 TERMINAL RAPID-FIRE TRIVIA QUIZ")
    print("=" * 65)

    while quiz.still_has_questions():
        try:
            q_text = quiz.next_question()
            ans = input(f"{q_text} (True/False): ").strip()
            if ans.lower() in ("exit", "q"):
                print("Exiting quiz early...")
                break
            if quiz.check_answer(ans):
                print(" ✅ Correct!\n")
            else:
                print(f" ❌ Wrong! The correct answer was {quiz.current_question.answer}.\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Quiz interrupted.")
            return

    print(f"🏆 Quiz Finished! Final Score: {quiz.score}/{quiz.question_number}\n")


def launch_gui_quiz():
    """Launches the Tkinter Desktop GUI Quizzer."""
    questions = build_question_bank()
    quiz = QuizBrain(questions)
    app = QuizInterface(quiz)
    app.run()


def main():
    print(logo)
    print("Welcome to Day 34 - Quizzler Trivia Studio! 🧠🏆\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🖥️ Launch Quizzler Desktop GUI (Tkinter + Live Trivia API)")
            print(" 2. ⚡ Play Terminal Trivia Quiz (CLI)")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                print("\n🚀 Launching Quizzler Desktop GUI Window...")
                launch_gui_quiz()
                print("✅ Quiz window closed.\n")
            elif choice == "2":
                run_terminal_quiz()
            elif choice == "3":
                print("\nExiting Quizzler Studio... Keep learning! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1, 2, or 3.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 34 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
