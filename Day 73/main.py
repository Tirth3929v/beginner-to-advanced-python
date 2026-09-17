"""
Day 73: Aggregate & Merge Data with Pandas
Phase 4: Data Science

Key Concepts:
GroupBy, Merge, Aggregation, Theme Tracking, LEGO Dataset Historical Analysis
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
    print(f" 🚀 DAY 73: AGGREGATE & MERGE DATA WITH PANDAS")
    print(f" 📚 Phase 4: Data Science | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: GroupBy, Merge, Aggregation, Theme Tracking, LEGO Dataset Historical Analysis\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 73/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 73 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
