"""
Day 31 - Flash Card Capstone Project Studio
Main launcher providing both Desktop GUI flash cards and Terminal CLI flash quiz.
"""

import csv
import os
import random
import sys
from art import logo
from flash_card_app import start_flash_card_app

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "french_words.csv")


def run_terminal_quiz():
    """Terminal-based rapid fire flash card quiz."""
    print("\n" + "=" * 65)
    print(" ⚡ TERMINAL RAPID-FIRE FLASH QUIZ")
    print("=" * 65)

    words = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            words = list(reader)
    except Exception as e:
        print(f"Error loading words: {e}")
        return

    if not words:
        print("No words found in word bank.")
        return

    sample_words = random.sample(words, min(5, len(words)))
    score = 0

    print("Translate the French word into English:\n")
    for i, w in enumerate(sample_words, 1):
        french = w["French"]
        english = w["English"].strip().lower()

        try:
            ans = input(f"[{i}/5] What is '{french}' in English? ").strip().lower()
            if ans == english:
                print(" ✅ Correct! Well done.\n")
                score += 1
            else:
                print(f" ❌ Incorrect! '{french}' translates to '{english}'.\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Quiz interrupted.")
            return

    print(f"🏆 Quiz Finished! Your Score: {score}/5\n")


def main():
    """Main execution loop for Day 31 Studio."""
    print(logo)
    print("Welcome to Day 31 - Flash Card Language Learning Capstone! 📇🇫🇷\n")

    try:
        while True:
            print("Choose an option:")
            print(" 1. 🖥️ Launch Desktop Flash Card GUI (Tkinter + Auto-Flip)")
            print(" 2. ⚡ Terminal Rapid-Fire Flash Card Quiz")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                print("\n🚀 Launching Flash Card Desktop Window...")
                start_flash_card_app()
                print("✅ Flash Card App closed.\n")
            elif choice == "2":
                run_terminal_quiz()
            elif choice == "3":
                print("\nExiting Day 31 Studio... Happy learning! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1, 2, or 3.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 31 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")
