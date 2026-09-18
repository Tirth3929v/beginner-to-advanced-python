"""
Day 49 - Automated LinkedIn Job Application Studio
Main launcher to execute LinkedIn job automation, auto-saving, and simulated applications.
"""

import sys
from art import logo
from linkedin_bot import (
    run_linkedin_bot,
    run_simulated_job_hunt,
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
    print("Welcome to Day 49 - Automated Job Applications Studio! 💼📑\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🚀 Run Automated LinkedIn Job Hunt (Simulated Pipeline)")
            print(" 2. 🌐 Launch Live Selenium Chrome Automation on LinkedIn")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                run_simulated_job_hunt()
            elif choice == "2":
                run_linkedin_bot()
            elif choice == "3":
                print("\nExiting Job Application Studio... Best of luck with your job hunt! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-3.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 49 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
