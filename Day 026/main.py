import sys
from art import logo
from comprehension_playground import run_comprehension_demos, run_nato_quiz
from nato_encoder import run_nato_encoder

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution menu for Day 26 - NATO Alphabet & Python Comprehensions."""
    print(logo)
    print("Welcome to Day 26 - List Comprehensions & NATO Phonetic Alphabet Studio! 📡🔤\n")

    try:
        while True:
            print("Choose an activity:")
            print(" 1. 🔤 NATO Phonetic Alphabet Word Translator")
            print(" 2. 🎯 NATO Aviation Spelling Quiz (Practice Mode)")
            print(" 3. 🧪 Comprehension Playground (List & Dict Demos)")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                run_nato_encoder()
            elif choice == "2":
                run_nato_quiz()
            elif choice == "3":
                run_comprehension_demos()
            elif choice == "4":
                print("\nExiting NATO Studio... Goodbye! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1, 2, 3, or 4.\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting NATO Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")

