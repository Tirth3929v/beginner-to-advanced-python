"""
Day 75: Beautiful Plotly Visualizations
Phase 4: Data Science

Key Concepts:
Plotly Express, Interactive Pie/Bar/Scatter Plots, Google Play Store Analytics
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
    print(f" 🚀 DAY 75: BEAUTIFUL PLOTLY VISUALIZATIONS")
    print(f" 📚 Phase 4: Data Science | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Plotly Express, Interactive Pie/Bar/Scatter Plots, Google Play Store Analytics\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 75/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 75 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
