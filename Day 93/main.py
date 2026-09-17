"""
Day 93: Automate Google Chrome Dinosaur Game
Phase 5: Portfolio

Key Concepts:
PyAutoGUI, Screen Capture, Pixel Color Detection, Jump Trigger Loop
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
    print(f" 🚀 DAY 93: AUTOMATE GOOGLE CHROME DINOSAUR GAME")
    print(f" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: PyAutoGUI, Screen Capture, Pixel Color Detection, Jump Trigger Loop\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 93/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 93 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
