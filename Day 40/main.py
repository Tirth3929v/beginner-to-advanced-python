"""
Day 40: Flight Club Capstone (Part 2)
Phase 2: Intermediate

Key Concepts:
Customer Acquisition, Email Notifications, Flight Price Comparison Engine
"""

import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def banner():
    """Prints the project banner."""
    print("=" * 70)
    print(f" 🚀 DAY 40: FLIGHT CLUB CAPSTONE (PART 2)")
    print(f" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Customer Acquisition, Email Notifications, Flight Price Comparison Engine\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 40/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 40 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
