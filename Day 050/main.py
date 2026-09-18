# -*- coding: utf-8 -*-
"""
Day 50: Auto Tinder Swiping Bot
Phase 2: Intermediate Capstone

Key Concepts:
Selenium Interactions, Modal Handling, Automated Swiping Loops, Error Recovery
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from tinder_bot import TinderBot


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 65)
    print(" 🚀 DAY 50: AUTOMATED TINDER SWIPING BOT (SELENIUM)")
    print(" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 65)
    print("Key Concepts: Selenium WebDriver, Modal Recovery, Keystroke Automation\n")


def run_project():
    banner()
    print("Choose an execution mode:")
    print(" 1) Run Interactive Simulation Engine (Safe, Offline Demo)")
    print(" 2) Launch Live Selenium Chrome Automation (Requires Local Browser)")
    print(" 3) Exit")

    choice = input("\nEnter choice (1-3) [default: 1]: ").strip() or "1"

    if choice == "1":
        count = input("Enter number of profiles to swipe [default: 6]: ").strip() or "6"
        try:
            swipes = max(1, min(int(count), 50))
        except ValueError:
            swipes = 6
        TinderBot.run_simulation(swipe_count=swipes)

    elif choice == "2":
        bot = TinderBot(headless=False)
        print("\nAttempting to connect to Chrome WebDriver...")
        if bot.init_driver():
            try:
                bot.live_auto_swipe(target_swipes=10)
            finally:
                bot.close()
        else:
            print("Falling back to simulation engine...")
            TinderBot.run_simulation(swipe_count=5)
    else:
        print("Exiting. Happy coding!")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Program interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()
