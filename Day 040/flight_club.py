"""
Day 40 - Flight Club Customer Acquisition & Broadcast Engine
Manages club user subscriptions with double email confirmation,
scans for bargain flight prices, and broadcasts email alerts with Google Flights booking links.
"""

import json
import os
import random
import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

MEMBERS_FILE = os.path.join(os.path.dirname(__file__), "club_members.json")

DEFAULT_MEMBERS = [
    {"firstName": "Tirth", "lastName": "Patel", "email": "tirthpatel82032@gmail.com"},
    {"firstName": "Emma", "lastName": "Watson", "email": "emma.watson@example.com"},
    {"firstName": "Liam", "lastName": "Davies", "email": "liam.traveler@example.com"}
]


class ClubManager:
    """Manages Flight Club customer registrations."""

    def __init__(self):
        self.members = self.load_members()

    def load_members(self) -> list:
        if os.path.exists(MEMBERS_FILE):
            try:
                with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        self.save_members(DEFAULT_MEMBERS)
        return DEFAULT_MEMBERS

    def save_members(self, data: list):
        self.members = data
        with open(MEMBERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def register_member(self, first_name: str, last_name: str, email: str, confirm_email: str) -> bool:
        """Validates matching emails and appends member to database."""
        if not first_name or not email:
            print("❌ First name and email are mandatory!")
            return False

        if email.strip().lower() != confirm_email.strip().lower():
            print("❌ Emails do not match! Registration aborted.")
            return False

        # Check for duplicates
        for m in self.members:
            if m["email"].lower() == email.strip().lower():
                print(f"ℹ️ {email} is already registered in Flight Club!")
                return True

        self.members.append({
            "firstName": first_name.strip().title(),
            "lastName": last_name.strip().title(),
            "email": email.strip().lower()
        })
        self.save_members(self.members)
        print(f"\n🎉 Welcome to Flight Club, {first_name}! You're in the club.")
        return True


class NotificationManager:
    """Formats and dispatches personalized flight deal notifications."""

    def __init__(self, club_manager: ClubManager):
        self.club = club_manager

    def broadcast_deal(self, deal: dict):
        """Sends an alert to all registered Flight Club members."""
        members = self.club.members
        if not members:
            print("No members found in Flight Club.")
            return

        origin = deal["origin_city"]
        origin_code = deal["origin_airport"]
        dest = deal["destination_city"]
        dest_code = deal["destination_airport"]
        price = deal["price"]
        out_d = deal["out_date"]
        ret_d = deal["return_date"]

        google_flights_link = (
            f"https://www.google.co.uk/flights?hl=en#flt={origin_code}.{dest_code}.{out_d}*{dest_code}.{origin_code}.{ret_d}"
        )

        print("\n" + "=" * 70)
        print(f" 💌 BROADCASTING FLIGHT DEAL TO {len(members)} CLUB MEMBER(S)")
        print("=" * 70)

        for person in members:
            name = person["firstName"]
            recipient = person["email"]

            subject = f"Low Price Alert: Fly to {dest} for only £{price:.2f}!"
            body = (
                f"Dear {name},\n\n"
                f"🚨 LOW PRICE ALERT! 🚨\n\n"
                f"Only £{price:.2f} to fly from {origin}-{origin_code} to {dest}-{dest_code},\n"
                f"from {out_d} to {ret_d}.\n\n"
                f"Book your flight now on Google Flights:\n{google_flights_link}\n\n"
                f"Happy Travels,\nYour Flight Club Team ✈️"
            )

            print(f" -> Sent notification to: {name} ({recipient})")

        print("=" * 70)
        print(f"✨ Sample Dispatched Email Payload:\n\nSubject: {subject}\n\n{body}\n")
