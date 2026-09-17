"""
Day 95: Custom 2D Racing Game
Phase 5: Portfolio

Key Concepts:
Turtle/Pygame 2D Engine, Obstacle Avoidance Vectors, Acceleration & Scores
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
    print(f" 🚀 DAY 95: CUSTOM 2D RACING GAME")
    print(f" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Turtle/Pygame 2D Engine, Obstacle Avoidance Vectors, Acceleration & Scores\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 95/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 95 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
