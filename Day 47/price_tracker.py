"""
Day 47 - Automated Amazon & E-Commerce Price Tracker
Scrapes product pages, extracts current prices, compares against target thresholds,
and automatically triggers email alerts when bargains are detected.
"""

import json
import os
import re
import smtplib
import sys
import urllib.request
from bs4 import BeautifulSoup

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WISHLIST_FILE = os.path.join(os.path.dirname(__file__), "wishlist.json")

# SMTP Configuration
MY_EMAIL = os.environ.get("MY_EMAIL", "price_tracker_bot@gmail.com")
MY_PASSWORD = os.environ.get("MY_EMAIL_PASSWORD", "demo_app_password")

DEFAULT_ITEMS = [
    {
        "title": "Instant Pot Duo 7-in-1 Electric Pressure Cooker, 6 Quart",
        "url": "https://www.amazon.com/dp/B00FLYWNYQ",
        "target_price": 79.99,
        "current_price": 69.95
    },
    {
        "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
        "url": "https://www.amazon.com/dp/B09XS7JWHH",
        "target_price": 348.00,
        "current_price": 329.99
    },
    {
        "title": "Logitech MX Master 3S Wireless Performance Mouse",
        "url": "https://www.amazon.com/dp/B09HM94VDS",
        "target_price": 99.99,
        "current_price": 99.99
    }
]


def load_wishlist() -> list:
    if os.path.exists(WISHLIST_FILE):
        try:
            with open(WISHLIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    with open(WISHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_ITEMS, f, indent=4)
    return DEFAULT_ITEMS


def scrape_amazon_price(url: str) -> float:
    """
    Scrapes product page using custom browser headers.
    Falls back to current cached price if CAPTCHA or network limits occur.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode("utf-8", errors="replace")
            soup = BeautifulSoup(html, "html.parser")

            # Common Amazon price class selectors
            price_element = soup.select_one("span.a-offscreen") or soup.select_one("span.a-price-whole")
            if price_element:
                raw_text = price_element.getText()
                cleaned = re.sub(r"[^\d.]", "", raw_text)
                if cleaned:
                    return float(cleaned)
    except Exception:
        pass
    return None


def send_price_alert(title: str, current_price: float, target_price: float, url: str):
    """Formats and dispatches email alert when item is cheaper than target budget."""
    subject = f"🚨 Amazon Price Drop Alert: {title[:40]}... is now ${current_price:.2f}!"
    body = (
        f"Great news!\n\n"
        f"The price for '{title}' has dropped below your target threshold of ${target_price:.2f}!\n"
        f"Current Price: ${current_price:.2f}\n"
        f"You save: ${target_price - current_price:.2f}\n\n"
        f"Buy it now on Amazon:\n{url}\n\n"
        f"Happy Shopping,\nYour Python Price Tracker 🛒"
    )

    print("\n" + "—" * 60)
    print(" 📧 [SIMULATED PRICE DROP EMAIL ALERT]")
    print(f" Subject: {subject}")
    print("—" * 60)
    print(body)
    print("—" * 60)


def check_all_prices():
    """Scans all wishlist items and notifies on price drops."""
    items = load_wishlist()
    print("\n" + "=" * 70)
    print(" 🛒 SCANNING E-COMMERCE WISHLIST PRICES")
    print("=" * 70)
    print(f" {'ITEM TITLE':32s} | {'TARGET':9s} | {'CURRENT':9s} | {'STATUS'}")
    print("=" * 70)

    alerts_triggered = 0

    for item in items:
        title = item["title"]
        target = item["target_price"]
        current = scrape_amazon_price(item["url"]) or item.get("current_price", target)

        short_title = title[:30] + "..." if len(title) > 30 else title
        if current < target:
            status = f"🔥 DEAL! (-${target - current:.2f})"
            alerts_triggered += 1
            print(f" {short_title:32s} | ${target:7.2f} | ${current:7.2f} | {status}")
            send_price_alert(title, current, target, item["url"])
        else:
            status = f"📈 Normal (${current:.2f})"
            print(f" {short_title:32s} | ${target:7.2f} | ${current:7.2f} | {status}")

    print("=" * 70)
    print(f"Scan complete: {alerts_triggered} price drop alert(s) triggered!\n")
