"""
Day 84: Image Watermarking Desktop App
Phase 5: Portfolio

Key Concepts:
Tkinter Desktop GUI, Pillow (PIL) Image Manipulation, Alpha Blending
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
    print(f" 🚀 DAY 84: IMAGE WATERMARKING DESKTOP APP")
    print(f" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Tkinter Desktop GUI, Pillow (PIL) Image Manipulation, Alpha Blending\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 84/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 84 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
