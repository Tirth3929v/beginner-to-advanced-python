# -*- coding: utf-8 -*-
"""
Day 52: Instagram Follower Bot
Phase 2: Intermediate Capstone

Key Concepts:
Selenium OOP Architecture, Modal Scrolling, Profile Navigation, Engagement Automation
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
from insta_follower import InstaFollower


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 68)
    print(" 🚀 DAY 52: INSTAGRAM FOLLOWER AUTOMATION BOT (SELENIUM)")
    print(" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 68)
    print("Key Concepts: Modal Scrolling, Follow Clicks, Anti-Ban Jitter, OOP Bot Design\n")


def run_project():
    banner()
    print("Choose an execution mode:")
    print(" 1) Run Interactive Target Audience Discovery Simulation (Safe, Offline)")
    print(" 2) Launch Live Instagram Automation Bot (Requires Chrome & Credentials)")
    print(" 3) Exit")

    choice = input("\nEnter choice (1-3) [default: 1]: ").strip() or "1"

    if choice == "1":
        target = input("Enter target account handle to scrape followers from [default: chefsteps]: ").strip() or "chefsteps"
        count = input("Enter number of accounts to follow [default: 5]: ").strip() or "5"
        try:
            max_f = max(1, min(int(count), 20))
        except ValueError:
            max_f = 5

        InstaFollower.run_simulation(target_account=target, max_follows=max_f)

    elif choice == "2":
        target = input("Enter target account handle to scrape followers from: ").strip() or "chefsteps"
        bot = InstaFollower(headless=False)
        print("\nAttempting to connect to Chrome WebDriver...")
        if bot.init_driver():
            try:
                if bot.live_login():
                    bot.live_find_followers(target_account=target)
                    bot.live_follow(max_follows=5)
            finally:
                bot.close()
        else:
            print("Chrome WebDriver unavailable. Running simulation mode instead...")
            InstaFollower.run_simulation(target_account=target, max_follows=5)
    else:
        print("Exiting. Happy coding!")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Program interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()
