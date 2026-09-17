"""
Day 40 - Flight Club Capstone Studio (Part 2)
Main launcher for Customer Acquisition, member database management, and broadcast alerts.
"""

import sys
from art import logo
from flight_club import ClubManager, NotificationManager

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def register_new_user(club: ClubManager):
    """Walks a user through joining Flight Club with double email verification."""
    print("\n" + "=" * 60)
    print(" 🛫 JOIN THE FLIGHT CLUB")
    print(" We find the best flight deals and email them to you directly.")
    print("=" * 60)

    first = input("👉 What is your first name? ").strip()
    last = input("👉 What is your last name? ").strip()
    email1 = input("👉 What is your email? ").strip()
    email2 = input("👉 Type your email again to confirm: ").strip()

    club.register_member(first, last, email1, email2)


def view_members(club: ClubManager):
    print("\n" + "=" * 60)
    print(f" {'FIRST NAME':15s} | {'LAST NAME':15s} | {'EMAIL'}")
    print("=" * 60)
    for m in club.members:
        print(f" {m['firstName']:15s} | {m['lastName']:15s} | {m['email']}")
    print("=" * 60)
    print(f" Total Registered Members: {len(club.members)}\n")


def simulate_deal_broadcast(club: ClubManager):
    """Generates an urgent flight bargain and broadcasts to all members."""
    notifier = NotificationManager(club)

    mock_deal = {
        "origin_city": "London",
        "origin_airport": "LON",
        "destination_city": "Tokyo",
        "destination_airport": "TYO",
        "price": 389.00,  # Below usual £485 budget
        "out_date": "2026-10-15",
        "return_date": "2026-10-28"
    }

    notifier.broadcast_deal(mock_deal)


def main():
    print(logo)
    print("Welcome to Day 40 - Flight Club Customer Acquisition Studio! ✈️💌\n")

    club = ClubManager()

    try:
        while True:
            print("Select an option:")
            print(" 1. ✍️ Register New Flight Club Member (Customer Acquisition)")
            print(" 2. 👥 View All Registered Club Members")
            print(" 3. 📢 Broadcast Flight Deal Alert to All Members")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                register_new_user(club)
            elif choice == "2":
                view_members(club)
            elif choice == "3":
                simulate_deal_broadcast(club)
            elif choice == "4":
                print("\nExiting Flight Club Studio... Have a great flight! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 40 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
