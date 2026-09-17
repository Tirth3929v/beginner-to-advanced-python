"""
Day 33 - ISS Overhead Notifier Studio
Interactive launcher to track the International Space Station in real time.
"""

import sys
import time
from art import logo
from iss_tracker import (
    DEFAULT_MY_LAT,
    DEFAULT_MY_LONG,
    check_iss_overhead,
    get_iss_position,
    is_night,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def display_status():
    """Runs a single live check and prints a structured mission control report."""
    print("\n🛰️  CONTACTING ISS TELEMETRY & SOLAR EPHEMERIS APIS...")
    report = check_iss_overhead(DEFAULT_MY_LAT, DEFAULT_MY_LONG)

    print("\n" + "=" * 65)
    print(" 🌍 MISSION CONTROL ORBITAL REPORT")
    print("=" * 65)
    print(f" Your Position:      Lat {report['user_lat']:+.4f}°, Lng {report['user_lng']:+.4f}°")
    print(f" Current ISS Orbit:  Lat {report['iss_lat']:+.4f}°, Lng {report['iss_lng']:+.4f}°")
    print(f" Distance to ISS:    {report['distance_km']:,} km")
    print(f" Position Proximity: {'✅ WITHIN VISUAL HORIZON (±5°)' if report['is_close'] else '❌ Outside visual horizon'}")
    print(f" Solar Lighting:     {'🌙 NIGHT-TIME (Sky is Dark)' if report['is_dark'] else '☀️ DAYTIME (Sunlight blinds orbit)'}")
    print("—" * 65)

    if report["is_visible"]:
        print(" 🎉 🚀 LOOK UP! The ISS is currently overhead in your night sky! 🌌✨")
        print(" (Simulating email/notification dispatch: 'ISS is visible overhead right now!')")
    else:
        print(" ℹ️ The ISS is not currently visible from your location.")
        if not report["is_close"]:
            print(f"    Reason: Too far away ({report['distance_km']} km away).")
        if not report["is_dark"]:
            print("    Reason: It is daylight at your coordinates.")
    print("=" * 65 + "\n")


def live_radar_loop():
    """Polls ISS coordinates in real-time loop."""
    print("\n📡 Launching Real-Time Orbital Radar (Press Ctrl+C to stop)...")
    print("=" * 65)
    print(f" {'TIMESTAMP':10s} | {'LATITUDE':12s} | {'LONGITUDE':12s} | {'STATUS'}")
    print("=" * 65)

    try:
        for _ in range(5):
            lat, lng, sim = get_iss_position()
            status = "📡 Live" if not sim else "🛰️ Orbit Sim"
            print(f" {time.strftime('%H:%M:%S'):10s} | {lat:+11.4f}° | {lng:+11.4f}° | {status}")
            time.sleep(2)
        print("=" * 65)
        print("✅ Radar scan completed.\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Radar stopped.\n")


def main():
    print(logo)
    print("Welcome to Day 33 - International Space Station Overhead Tracker! 🛰️🌌\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🛰️ Check ISS Overhead Status (Single Check & Alert)")
            print(" 2. 📡 Run Real-Time Orbital Radar (5 Live pings)")
            print(" 3. ☀️ Check Local Sunrise & Sunset Times")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                display_status()
            elif choice == "2":
                live_radar_loop()
            elif choice == "3":
                dark, sr, ss, sim = is_night(DEFAULT_MY_LAT, DEFAULT_MY_LONG)
                print(f"\n☀️ Solar Report for ({DEFAULT_MY_LAT}, {DEFAULT_MY_LONG}):")
                print(f" • Sunrise: {sr:02d}:00 UTC | Sunset: {ss:02d}:00 UTC")
                print(f" • Current state: {'🌙 Night' if dark else '☀️ Day'}\n")
            elif choice == "4":
                print("\nExiting ISS Tracker... Clear skies! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 33 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
