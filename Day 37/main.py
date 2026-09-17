"""
Day 37 - Pixela Habit Tracking Studio
Interactive launcher to log daily habits, update entries, and view habit heatmaps.
"""

import datetime as dt
import sys
from art import logo
from pixela_tracker import (
    DEFAULT_GRAPH_ID,
    DEFAULT_USERNAME,
    create_graph,
    create_user,
    delete_habit_pixel,
    log_habit_pixel,
    print_terminal_heatmap,
    update_habit_pixel,
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
    print("Welcome to Day 37 - Pixela Habit Tracker & Streak Studio! 📊🟩\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🟩 Log Habit Progress for Today (HTTP POST)")
            print(" 2. 📅 Log Habit Progress for a Custom Date (YYYYMMDD)")
            print(" 3. ✏️ Update an Existing Habit Record (HTTP PUT)")
            print(" 4. 🗑️ Delete an Incorrect Habit Record (HTTP DELETE)")
            print(" 5. 🗺️ View Visual Terminal Habit Heatmap")
            print(" 6. 🚀 Setup New Pixela Cloud Account & Graph")
            print(" 7. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-7): ").strip()
            if choice == "1":
                try:
                    hrs = float(input("👉 Hours spent coding/studying today: ").strip())
                    log_habit_pixel(hrs)
                except ValueError:
                    print("⚠️ Please enter a valid decimal number (e.g. 2.5)!")

            elif choice == "2":
                date_input = input("👉 Enter date in YYYYMMDD format (e.g. 20260915): ").strip()
                try:
                    hrs = float(input(f"👉 Hours spent on {date_input}: ").strip())
                    log_habit_pixel(hrs, date_str=date_input)
                except ValueError:
                    print("⚠️ Invalid hours number!")

            elif choice == "3":
                date_input = input("👉 Enter date to update (YYYYMMDD): ").strip()
                try:
                    hrs = float(input(f"👉 New corrected hours for {date_input}: ").strip())
                    update_habit_pixel(hrs, date_str=date_input)
                except ValueError:
                    print("⚠️ Invalid hours number!")

            elif choice == "4":
                date_input = input("👉 Enter date to delete (YYYYMMDD): ").strip()
                confirm = input(f"⚠️ Are you sure you want to delete pixel for {date_input}? (y/n): ").strip().lower()
                if confirm == "y":
                    delete_habit_pixel(date_input)

            elif choice == "5":
                print_terminal_heatmap()

            elif choice == "6":
                u = input(f"Username [{DEFAULT_USERNAME}]: ").strip() or DEFAULT_USERNAME
                t = input("Token (min 8 chars): ").strip() or "secretToken12345"
                create_user(u, t)
                create_graph(u, t, DEFAULT_GRAPH_ID, "Daily Python Study")

            elif choice == "7":
                print("\nExiting Pixela Studio... Keep building habits! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-7.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 37 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
