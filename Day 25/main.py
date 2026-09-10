import sys
from art import logo
from squirrel_census import run_squirrel_census_analysis
from us_states_game import run_us_states_game

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution menu for Day 25 - CSV Data & Pandas Analytics."""
    print(logo)
    print("Welcome to Day 25 - CSV Data Processing & Pandas Analytics Studio! 🐼🗺️\n")

    print("Choose a project to launch:")
    print(" 1. 🗺️  50 U.S. States Interactive Map Quiz Game")
    print(" 2. 🐿️ Central Park Squirrel Census Data Analysis")
    print(" 3. 🚪 Exit\n")

    try:
        choice = input("👉 Enter choice (1-3): ").strip()
        if choice == "1":
            run_us_states_game()
        elif choice == "2":
            run_squirrel_census_analysis()
        elif choice == "3":
            print("Goodbye! 👋")
        else:
            print("Invalid choice! Launching Squirrel Census Analysis by default...")
            run_squirrel_census_analysis()
    except Exception as e:
        print(f"\n⚠️ Note: GUI display requires interactive window environment. ({e})")


if __name__ == "__main__":
    main()
