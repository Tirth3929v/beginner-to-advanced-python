"""
Day 39 - Flight Deal Finder Studio (Part 1 Capstone)
Scans destination thresholds, queries flight search engine, and alerts on price drops.
"""

import sys
from art import logo
from data_manager import DataManager
from flight_search import FlightSearch

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def scan_for_flight_deals():
    """Scans all tracked destinations and reports any deals below target budget."""
    data_mgr = DataManager()
    searcher = FlightSearch(origin_city="London", origin_iata="LON")

    print("\n" + "=" * 70)
    print(" ✈️ SCANNING GLOBAL FLIGHT FARES (ORIGIN: LON - LONDON)")
    print("=" * 70)
    print(f" {'CITY':15s} | {'IATA':5s} | {'TARGET':8s} | {'CURRENT':9s} | {'STATUS'}")
    print("=" * 70)

    deals_found = []

    for dest in data_mgr.destinations:
        city = dest["city"]
        iata = dest["iataCode"]
        target = dest["lowestPrice"]

        flight = searcher.check_flights(city, iata, target)
        current = flight.price

        if current < target:
            status = f"🔥 DEAL! (-£{target - current:.2f})"
            deals_found.append(flight)
        else:
            status = f"📈 Normal (+£{current - target:.2f})"

        print(f" {city:15s} | {iata:5s} | £{target:6.2f} | £{current:7.2f} | {status}")

    print("=" * 70)

    if deals_found:
        print(f"\n🎉 FOUND {len(deals_found)} FLIGHT DEAL(S) BELOW TARGET BUDGET!\n")
        for i, deal in enumerate(deals_found, 1):
            print(f"--- BARGAIN DEAL #{i} ---")
            print(deal)
            print()
    else:
        print("\nℹ️ No flights found below target budget today. Continuing surveillance!\n")


def view_destinations():
    data_mgr = DataManager()
    print("\n" + "=" * 50)
    print(f" {'CITY':20s} | {'IATA':6s} | {'BUDGET TARGET'}")
    print("=" * 50)
    for d in data_mgr.destinations:
        print(f" {d['city']:20s} | {d['iataCode']:6s} | £{d['lowestPrice']:.2f}")
    print("=" * 50 + "\n")


def main():
    print(logo)
    print("Welcome to Day 39 - Flight Deal Finder Studio! ✈️🌍\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🔍 Scan All Tracked Flight Routes for Low Fare Deals")
            print(" 2. 📋 View Tracked Destinations & Target Prices")
            print(" 3. ➕ Add New Destination Route")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                scan_for_flight_deals()
            elif choice == "2":
                view_destinations()
            elif choice == "3":
                c = input(" Destination City: ").strip()
                code = input(" 3-Letter IATA Code (e.g. DXB, ROM, BCN): ").strip().upper()
                try:
                    price = float(input(" Target Budget Price in £: ").strip())
                    DataManager().add_destination(c, code, price)
                    print(f"✅ Added {c} ({code}) with target budget £{price:.2f}!\n")
                except ValueError:
                    print("⚠️ Invalid price number!\n")
            elif choice == "4":
                print("\nExiting Flight Deal Finder... Safe travels! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 39 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
