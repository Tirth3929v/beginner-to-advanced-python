import sys
from art import logo
from etch_a_sketch import run_etch_a_sketch
from turtle_race import start_turtle_race

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution menu for Day 19 projects."""
    print(logo)
    print("Welcome to Day 19 - Instances, State & Higher Order Functions! 🐢🎮\n")

    print("Choose a project to launch:")
    print(" 1. 🐢🏁 Ultimate Turtle Race (Multi-Instance OOP Game)")
    print(" 2. ✏️🎨 Etch-A-Sketch Interactive Drawing App")
    print(" 3. 🚪 Exit\n")

    try:
        choice = input("👉 Enter choice (1-3): ").strip()
        if choice == "1":
            start_turtle_race()
        elif choice == "2":
            run_etch_a_sketch()
        elif choice == "3":
            print("Goodbye! 👋")
        else:
            print("Invalid choice! Launching Turtle Race by default...")
            start_turtle_race()
    except Exception as e:
        print(f"\n⚠️ Note: GUI display requires interactive window environment. ({e})")


if __name__ == "__main__":
    main()
