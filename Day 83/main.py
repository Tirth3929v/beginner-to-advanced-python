"""
Day 83: Tic Tac Toe Python Game with AI
Phase 5: Portfolio

Key Concepts:
Game Theory, Minimax Decision Algorithm, 2-Player CLI & Interactive Board
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
    print(f" 🚀 DAY 83: TIC TAC TOE PYTHON GAME WITH AI")
    print(f" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Game Theory, Minimax Decision Algorithm, 2-Player CLI & Interactive Board\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 83/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 83 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
