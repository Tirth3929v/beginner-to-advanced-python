"""
Day 32 - Automated Birthday Wisher & Monday Motivation Studio
Interactive launcher connecting quotes, birthday scanners, and template dispatchers.
"""

import sys
from art import logo
from birthday_wisher import (
    add_new_birthday,
    check_and_send_birthdays,
    get_random_quote,
    list_birthdays,
    run_monday_motivation,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    print(logo)
    print("Welcome to Day 32 - Automated Birthday Wisher & Motivation Studio! 🎂💌\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🔍 Scan & Send Today's Birthday Wishes (Automated)")
            print(" 2. ⚡ Send Monday Motivation Quote (Now)")
            print(" 3. 📋 View All Stored Birthdays")
            print(" 4. ➕ Add New Birthday Entry")
            print(" 5. 🎲 Preview Random Motivational Quote")
            print(" 6. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-6): ").strip()
            if choice == "1":
                check_and_send_birthdays()
            elif choice == "2":
                run_monday_motivation(force=True)
            elif choice == "3":
                list_birthdays()
            elif choice == "4":
                name = input(" Name: ").strip()
                if not name:
                    print("⚠️ Name cannot be empty!\n")
                    continue
                email = input(" Email: ").strip()
                if not email:
                    email = f"{name.lower().replace(' ', '.')}@example.com"
                try:
                    year_inp = input(" Birth Year (default 2000): ").strip()
                    year = int(year_inp) if year_inp else 2000
                    month = int(input(" Birth Month (1-12): ").strip())
                    day = int(input(" Birth Day (1-31): ").strip())
                    if not (1 <= month <= 12 and 1 <= day <= 31):
                        print("⚠️ Invalid month or day!\n")
                        continue
                    add_new_birthday(name, email, year, month, day)
                except ValueError:
                    print("⚠️ Please enter valid numbers for year, month, and day!\n")
            elif choice == "5":
                q = get_random_quote()
                print(f"\n✨ Quote: {q}\n")
            elif choice == "6":
                print("\nExiting Day 32 Studio... Have a great day! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please choose 1-6.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 32 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
