import sys
from art import logo
from dynamic_typing_demo import run_dynamic_typing_demos
from pomodoro_app import start_pomodoro_app

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution menu for Day 28 - Pomodoro Productivity Studio."""
    print(logo)
    print("Welcome to Day 28 - Pomodoro Desktop Timer & Dynamic Typing Studio! 🍅⏱️\n")

    try:
        while True:
            print("Choose an option to launch:")
            print(" 1. 🍅 Launch Pomodoro Desktop Focus App (GUI)")
            print(" 2. ⚡ Python Dynamic Typing Interactive Lesson")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                print("\n🚀 Launching Pomodoro Focus Desktop Window...")
                start_pomodoro_app()
                print("✅ App closed.\n")
            elif choice == "2":
                run_dynamic_typing_demos()
            elif choice == "3":
                print("\nExiting Pomodoro Studio... Happy Coding! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1, 2, or 3.\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Pomodoro Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")
