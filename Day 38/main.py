"""
Day 38 - Workout Tracking Studio
Interactive natural language exercise logger connecting to Nutritionix & Google Sheets.
"""

import sys
from art import logo
from workout_tracker import (
    log_workout_to_sheety,
    parse_exercises_nlp,
    view_workout_history,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def record_workout():
    """Prompts user in plain English, calculates calories, and saves to journal."""
    print("\n👉 Tell me what exercises you did in plain English:")
    print("   Example: 'Ran 3 miles and walked for 20 minutes', or 'Did 45 mins of yoga'")
    user_input = input("\n🗣️ Your workout: ").strip()

    if not user_input:
        print("⚠️ Workout entry cannot be empty!")
        return

    print("\n🧠 Parsing exercises with Natural Language Processing...")
    exercises = parse_exercises_nlp(user_input)

    if not exercises:
        print("❌ Could not identify specific exercises.")
        return

    print("\n" + "=" * 65)
    print(" 📊 CALCULATED EXERCISE BREAKDOWN")
    print("=" * 65)
    for ex in exercises:
        name = ex.get("name", "Exercise").title()
        dur = ex.get("duration_min", 30)
        cal = ex.get("nf_calories", 150)
        print(f" • {name:20s} -> Duration: {dur} mins | Calories: {cal} kcal")
        log_workout_to_sheety(name, dur, cal)
    print("=" * 65)
    print("✅ All exercises committed to workout database!\n")


def main():
    print(logo)
    print("Welcome to Day 38 - Natural Language Workout Tracker Studio! 🏋️📊\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🗣️ Log Workout via Natural Language (NLP Engine)")
            print(" 2. 📋 View Logged Workout Journal & Total Calories")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                record_workout()
            elif choice == "2":
                view_workout_history()
            elif choice == "3":
                print("\nExiting Workout Tracker... Keep fit! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1, 2, or 3.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 38 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
