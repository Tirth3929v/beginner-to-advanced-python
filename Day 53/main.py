# -*- coding: utf-8 -*-
"""
Day 53: Web Scraping Capstone - Rental Research
Phase 2: Intermediate Capstone

Key Concepts:
BeautifulSoup4 Parsing, Regex Sanitization, CSV Export, Selenium Google Form Automation
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
from rental_research import RentalResearcher


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 68)
    print(" 🚀 DAY 53: RENTAL RESEARCH WEB SCRAPING CAPSTONE")
    print(" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 68)
    print("Key Concepts: BS4 Parsing, Regex Sanitization, Selenium Google Forms\n")


def run_project():
    banner()
    print("Choose an execution mode:")
    print(" 1) Run Scraping, Sanitization & Form Submission Simulation (Safe, Offline)")
    print(" 2) Scrape Live Clone & Export CSV Only (No Browser Needed)")
    print(" 3) Launch Live Scraping + Selenium Google Form Automation")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        count = input("Enter number of listings to process [default: 4]: ").strip() or "4"
        try:
            n = max(1, min(int(count), 20))
        except ValueError:
            n = 4
        RentalResearcher.run_simulation(max_entries=n)

    elif choice == "2":
        bot = RentalResearcher()
        bot.scrape_listings()
        out = bot.export_csv("rentals_export.csv")
        print(f"\n✨ Export complete! Open '{out}' in Excel or Google Sheets.")

    elif choice == "3":
        form_url = input("Enter your Google Form URL: ").strip()
        if not form_url:
            print("No URL provided. Running simulation instead...")
            RentalResearcher.run_simulation(max_entries=4)
            return

        bot = RentalResearcher(google_form_url=form_url)
        bot.scrape_listings()
        bot.export_csv()
        print("\nAttempting to connect to Chrome WebDriver...")
        if bot.init_driver(headless=False):
            try:
                bot.live_fill_form(form_url)
            finally:
                bot.close()
        else:
            print("Chrome WebDriver unavailable.")
    else:
        print("Exiting. Happy coding!")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Program interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()
