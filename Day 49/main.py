"""
Day 49: Automated Job Applications on LinkedIn
Phase 2: Intermediate

Key Concepts:
Selenium Form Filling, Login Handling, Exception Handling in Automation
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
    print(f" 🚀 DAY 49: AUTOMATED JOB APPLICATIONS ON LINKEDIN")
    print(f" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Selenium Form Filling, Login Handling, Exception Handling in Automation\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 49/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 49 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
