"""
Day 45 - Web Scraping with BeautifulSoup4 Studio
Main launcher to run movie scrapers, Hacker News trending stories, and file exports.
"""

import sys
from art import logo
from movie_scraper import (
    scrape_hacker_news,
    scrape_top_movies,
    view_saved_movies,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def display_hn_top_story():
    story = scrape_hacker_news()
    print("\n" + "=" * 65)
    print(" 🔥 TOP TRENDING HACKER NEWS STORY")
    print("=" * 65)
    print(f" Headline:  {story['title']}")
    print(f" Upvotes:   🔺 {story['score']} points")
    print(f" Article:   {story['link']}")
    print("=" * 65 + "\n")


def main():
    print(logo)
    print("Welcome to Day 45 - Web Scraping with BeautifulSoup4 Studio! 🥣🌐\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🎬 Scrape Empire Top 100 Movies to 'movies.txt'")
            print(" 2. 📋 View Saved Movies from 'movies.txt'")
            print(" 3. 🔥 Scrape Top Trending Hacker News Story")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                scrape_top_movies()
            elif choice == "2":
                view_saved_movies()
            elif choice == "3":
                display_hn_top_story()
            elif choice == "4":
                print("\nExiting Web Scraping Studio... Happy scraping! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 45 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
