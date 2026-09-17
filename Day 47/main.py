"""
Day 47 - Automated Amazon Price Tracker Studio
Main launcher to monitor product prices and dispatch automated deal alerts.
"""

import json
import sys
from art import logo
from price_tracker import (
    WISHLIST_FILE,
    check_all_prices,
    load_wishlist,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def add_tracked_item():
    """Adds a new item to the wishlist."""
    title = input("👉 Enter Product Name: ").strip()
    url = input("👉 Enter Product URL: ").strip()
    try:
        target = float(input("👉 Enter Target Alert Price (e.g. 99.99): ").strip())
        items = load_wishlist()
        items.append({
            "title": title,
            "url": url,
            "target_price": target,
            "current_price": target
        })
        with open(WISHLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=4)
        print(f"✅ Successfully added '{title}' to tracking wishlist!\n")
    except ValueError:
        print("⚠️ Invalid target price number!\n")


def view_wishlist():
    items = load_wishlist()
    print("\n" + "=" * 65)
    print(f" {'PRODUCT':35s} | {'TARGET PRICE':14s} | {'CURRENT'}")
    print("=" * 65)
    for it in items:
        t = it["title"][:32] + "..." if len(it["title"]) > 32 else it["title"]
        print(f" {t:35s} | ${it['target_price']:12.2f} | ${it.get('current_price', 0):.2f}")
    print("=" * 65 + "\n")


def main():
    print(logo)
    print("Welcome to Day 47 - Amazon Price Tracker Studio! 🛒📉\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🔍 Scan Wishlist for Price Drops & Trigger Alerts")
            print(" 2. 📋 View Tracked Products in Wishlist")
            print(" 3. ➕ Add New Product to Wishlist")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                check_all_prices()
            elif choice == "2":
                view_wishlist()
            elif choice == "3":
                add_tracked_item()
            elif choice == "4":
                print("\nExiting Price Tracker... Happy deal hunting! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 47 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
