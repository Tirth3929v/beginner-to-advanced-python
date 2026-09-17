"""
Day 51: Internet Speed Twitter Complaint Bot
Phase 2: Intermediate

Key Concepts:
Speedtest CLI, Selenium Automation, Twitter/X Login & Tweeting
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
    print(f" 🚀 DAY 51: INTERNET SPEED TWITTER COMPLAINT BOT")
    print(f" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Speedtest CLI, Selenium Automation, Twitter/X Login & Tweeting\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 51/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 51 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
