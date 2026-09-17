"""
Day 48: Selenium Webdriver Automation & Cookie Bot
Phase 2: Intermediate

Key Concepts:
Selenium Webdriver, XPath Selectors, Browser Automation, Game Bot
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
    print(f" 🚀 DAY 48: SELENIUM WEBDRIVER AUTOMATION & COOKIE BOT")
    print(f" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Selenium Webdriver, XPath Selectors, Browser Automation, Game Bot\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 48/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 48 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
