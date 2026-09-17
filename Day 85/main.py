"""
Day 85: Typing Speed Test Desktop App
Phase 5: Portfolio

Key Concepts:
Tkinter Canvas, Timer Callbacks, Live WPM & Character Accuracy Calculation
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
    print(f" 🚀 DAY 85: TYPING SPEED TEST DESKTOP APP")
    print(f" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Tkinter Canvas, Timer Callbacks, Live WPM & Character Accuracy Calculation\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 85/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 85 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
