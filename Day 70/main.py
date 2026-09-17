"""
Day 70: Version Control Mastery with Git & GitHub
Phase 4: Data Science

Key Concepts:
Branching, Merging, Rebasing, Conflict Resolution, Git CLI Best Practices
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
    print(f" 🚀 DAY 70: VERSION CONTROL MASTERY WITH GIT & GITHUB")
    print(f" 📚 Phase 4: Data Science | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Branching, Merging, Rebasing, Conflict Resolution, Git CLI Best Practices\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 70/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 70 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
