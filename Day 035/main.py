"""
Day 35 - SMS Weather Rain Alert Studio
Main launcher to check forecast, inspect weather codes, and test rain SMS alerts.
"""

import sys
from art import logo
from rain_alert import (
    DEFAULT_LAT,
    DEFAULT_LON,
    check_rain_and_alert,
    send_sms_alert,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    print(logo)
    print("Welcome to Day 35 - SMS Rain Alert & Weather Forecast Studio! 🌧️📱\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🔍 Scan 12-Hour Weather & Auto-Trigger Rain Alert")
            print(" 2. 📱 Test Custom SMS Dispatcher")
            print(" 3. 🌐 Check Weather for Custom Coordinates (Lat/Lon)")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                check_rain_and_alert(DEFAULT_LAT, DEFAULT_LON)
            elif choice == "2":
                msg = input("Enter test SMS message text: ").strip()
                if not msg:
                    msg = "🌧️ Test Alert: Remember to bring an umbrella! ☔"
                send_sms_alert(msg)
            elif choice == "3":
                try:
                    lat = float(input(" Enter Latitude (e.g. 51.5074 for London): ").strip())
                    lon = float(input(" Enter Longitude (e.g. -0.1278 for London): ").strip())
                    check_rain_and_alert(lat, lon)
                except ValueError:
                    print("⚠️ Invalid coordinate numbers!")
            elif choice == "4":
                print("\nExiting Day 35 Studio... Stay dry! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 35 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
