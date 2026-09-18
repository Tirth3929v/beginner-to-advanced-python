"""
Day 46 - Musical Time Machine Studio
Main launcher to scrape historical Billboard charts and generate throwback Spotify playlists.
"""

import datetime as dt
import sys
from art import logo
from spotify_time_machine import (
    create_spotify_playlist,
    scrape_billboard_hot_100,
    view_playlist,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def time_travel_to_date():
    """Prompts for date, scrapes Billboard, and builds playlist."""
    print("\n🕰️  WHICH YEAR DO YOU WANT TO TRAVEL TO?")
    date_input = input("👉 Enter date in YYYY-MM-DD format (e.g. 2000-08-12): ").strip()

    if not date_input:
        date_input = "2000-08-12"
        print(f"Using default date: {date_input}")

    songs = scrape_billboard_hot_100(date_input)
    if songs:
        create_spotify_playlist(date_input, songs)
        view_playlist(date_input)


def main():
    print(logo)
    print("Welcome to Day 46 - Musical Time Machine & Spotify Playlist Studio! 🎵📻\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🚀 Travel Back in Time & Create Playlist (Custom Date)")
            print(" 2. 🎸 Quick Travel to the Year 2000 (2000-08-12)")
            print(" 3. 💾 View Saved Throwback Playlist")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                time_travel_to_date()
            elif choice == "2":
                songs = scrape_billboard_hot_100("2000-08-12")
                create_spotify_playlist("2000-08-12", songs)
                view_playlist("2000-08-12")
            elif choice == "3":
                d = input("Enter date of playlist (YYYY-MM-DD): ").strip()
                view_playlist(d)
            elif choice == "4":
                print("\nExiting Musical Time Machine... Rock on! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 46 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
