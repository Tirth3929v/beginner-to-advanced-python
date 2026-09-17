"""
Day 36: Stock Trading News Alert Project
Phase 2: Intermediate

Key Concepts:
Alpha Vantage API, NewsAPI, Percent Price Shift Calculation, SMS/Email Alerts
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
    print(f" 🚀 DAY 36: STOCK TRADING NEWS ALERT PROJECT")
    print(f" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Alpha Vantage API, NewsAPI, Percent Price Shift Calculation, SMS/Email Alerts\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 36/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 36 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
