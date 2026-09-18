# -*- coding: utf-8 -*-
"""
Day 51: Internet Speed Twitter Complaint Bot
Phase 2: Intermediate Capstone

Key Concepts:
Bandwidth Benchmarking, Selenium Interactions, Twitter/X Automation, SLA Monitoring
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
from speed_twitter_bot import InternetSpeedTwitterBot


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 68)
    print(" 🚀 DAY 51: INTERNET SPEED TWITTER COMPLAINT BOT (SELENIUM)")
    print(" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 68)
    print("Key Concepts: Speedtest Diagnostics, SLA Calculation, Automated Tweeting\n")


def run_project():
    banner()
    print("Choose an execution mode:")
    print(" 1) Run Interactive Bandwidth SLA Audit & Tweet Simulation (Safe, Offline)")
    print(" 2) Launch Live Speedtest & Twitter Automation via Chrome WebDriver")
    print(" 3) Exit")

    choice = input("\nEnter choice (1-3) [default: 1]: ").strip() or "1"

    if choice == "1":
        down_in = input("Enter your promised download speed (Mbps) [default: 150]: ").strip() or "150"
        up_in = input("Enter your promised upload speed (Mbps) [default: 25]: ").strip() or "25"
        isp_in = input("Enter your ISP Twitter handle (e.g. Comcast, ATTHelp) [default: Comcast]: ").strip() or "Comcast"

        try:
            p_down = float(down_in)
            p_up = float(up_in)
        except ValueError:
            p_down, p_up = 150.0, 25.0

        bot = InternetSpeedTwitterBot(promised_down=p_down, promised_up=p_up, isp_handle=isp_in)
        bot.simulate_test(force_throttle=True)

    elif choice == "2":
        bot = InternetSpeedTwitterBot(headless=False)
        print("\nAttempting to connect to Chrome WebDriver...")
        if bot.init_driver():
            try:
                down, up = bot.live_get_internet_speed()
                if down < bot.promised_down or up < bot.promised_up:
                    bot.live_tweet_at_provider()
                else:
                    print("Speed is within acceptable limits. No tweet sent.")
            finally:
                bot.close()
        else:
            print("Chrome WebDriver unavailable. Running simulation mode instead...")
            bot.simulate_test(force_throttle=True)
    else:
        print("Exiting. Happy coding!")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Program interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()
