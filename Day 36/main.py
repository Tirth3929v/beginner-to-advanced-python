"""
Day 36 - Stock Trading News Alert Studio
Main launcher to monitor stock price swings and dispatch automated news alerts.
"""

import sys
from art import logo
from stock_alert import (
    DEFAULT_COMPANY,
    DEFAULT_STOCK,
    THRESHOLD_PERCENT,
    generate_stock_alerts,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_alert_scan(symbol=DEFAULT_STOCK, company=DEFAULT_COMPANY, threshold=THRESHOLD_PERCENT):
    """Executes a full volatility scan and displays formatted SMS alert payloads."""
    alerts = generate_stock_alerts(symbol, company, threshold)
    if alerts:
        print("\n" + "=" * 65)
        print(" 📱 DISPATCHED SMS ALERTS")
        print("=" * 65)
        for idx, alert_text in enumerate(alerts, 1):
            print(f"--- ALERT #{idx} ---")
            print(alert_text)
            print()
        print("=" * 65)
        print("✨ All alerts formatted and dispatched successfully!\n")


def main():
    print(logo)
    print("Welcome to Day 36 - Stock Trading News Alert Studio! 📈📰\n")

    try:
        while True:
            print("Select an option:")
            print(f" 1. 🔍 Scan Default Stock ({DEFAULT_STOCK} - {DEFAULT_COMPANY})")
            print(" 2. 🎯 Scan Custom Ticker & Company Name")
            print(" 3. ⚙️ Adjust Volatility Alert Sensitivity Threshold")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                run_alert_scan()
            elif choice == "2":
                sym = input(" Enter Stock Ticker (e.g. AAPL, MSFT, GOOGL): ").strip().upper()
                comp = input(" Enter Company Name (e.g. Apple Inc, Microsoft): ").strip()
                if sym and comp:
                    run_alert_scan(sym, comp)
                else:
                    print("⚠️ Ticker and Company cannot be empty!")
            elif choice == "3":
                try:
                    new_thresh = float(input(" Enter new threshold percentage (e.g. 2.0 or 5.0): ").strip())
                    run_alert_scan(DEFAULT_STOCK, DEFAULT_COMPANY, new_thresh)
                except ValueError:
                    print("⚠️ Invalid percentage number!")
            elif choice == "4":
                print("\nExiting Stock Alert Studio... Good trading! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 36 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
