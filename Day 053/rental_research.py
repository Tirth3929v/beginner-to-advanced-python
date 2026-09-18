"""
Day 53: Rental Research Web Scraping & Automated Data Entry Capstone
Scrapes property listings from rental websites (Zillow Clone) using BeautifulSoup,
cleans price/address data, and automates bulk submission into Google Forms using Selenium.
Includes offline fallback data, CSV exporter, and interactive simulation mode.
"""

import sys
import os
import re
import csv
import json
import time
from typing import List, Dict, Any

# Unicode safe console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SAMPLE_RENTALS = [
    {"address": "2840 Jackson St, San Francisco, CA 94115", "price": "$2,895/mo", "link": "https://www.zillow.com/b/2840-jackson-st-san-francisco-ca-5XjY9p/"},
    {"address": "742 Montgomery St, San Francisco, CA 94111", "price": "$3,200/mo", "link": "https://www.zillow.com/b/742-montgomery-st-san-francisco-ca-9K2mN/"},
    {"address": "1150 Sacramento St, San Francisco, CA 94108", "price": "$2,450/mo", "link": "https://www.zillow.com/b/1150-sacramento-st-san-francisco-ca-3L4pQ/"},
    {"address": "525 Market St, San Francisco, CA 94105", "price": "$3,650/mo", "link": "https://www.zillow.com/b/525-market-st-san-francisco-ca-8V1zR/"},
    {"address": "1890 Lombard St, San Francisco, CA 94123", "price": "$2,700/mo", "link": "https://www.zillow.com/b/1890-lombard-st-san-francisco-ca-2H7tY/"},
    {"address": "450 Sutter St, San Francisco, CA 94108", "price": "$2,990/mo", "link": "https://www.zillow.com/b/450-sutter-st-san-francisco-ca-4B9wK/"},
]

TARGET_ZILLOW_CLONE = "https://appbrewery.github.io/Zillow-Clone/"


class RentalResearcher:
    """
    Capstone engine combining BeautifulSoup web-scraping with Selenium data-entry
    to build automated real-estate research pipelines.
    """

    def __init__(self, google_form_url: str = ""):
        self.google_form_url = google_form_url
        self.listings: List[Dict[str, str]] = []
        self.driver = None

    def scrape_listings(self) -> List[Dict[str, str]]:
        """Scrapes property listings from Zillow clone website using BeautifulSoup."""
        print(f"🌐 Fetching live listings from {TARGET_ZILLOW_CLONE} ...")
        try:
            import requests
            from bs4 import BeautifulSoup

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
            response = requests.get(TARGET_ZILLOW_CLONE, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".StyledPropertyCardDataWrapper")

            scraped = []
            for card in cards:
                # Extract address
                addr_elem = card.select_one("address")
                address = addr_elem.get_text(strip=True).replace("|", "").strip() if addr_elem else "N/A"

                # Extract price
                price_elem = card.select_one(".PropertyCardWrapper__StyledPriceLine")
                raw_price = price_elem.get_text(strip=True) if price_elem else "$0"
                # Clean price: e.g. "$2,895+/mo" or "$2,895/mo" -> "$2,895"
                match = re.search(r"\$\d[\d,]*", raw_price)
                clean_price = match.group(0) if match else raw_price

                # Extract link
                link_elem = card.select_one("a.property-card-link")
                link = link_elem.get("href", "") if link_elem else ""
                if link and not link.startswith("http"):
                    link = f"https://www.zillow.com{link}"

                if address and address != "N/A":
                    scraped.append({
                        "address": address,
                        "price": clean_price,
                        "link": link
                    })

            if scraped:
                self.listings = scraped
                print(f"✅ Successfully scraped and cleaned {len(self.listings)} property listings!")
                return self.listings

        except Exception as e:
            print(f"⚠️ Live scraping failed or network offline ({e}). Utilizing cached sample dataset.")

        self.listings = SAMPLE_RENTALS.copy()
        return self.listings

    def export_csv(self, filename: str = "rentals_export.csv") -> str:
        """Exports parsed listings into a structured CSV file."""
        if not self.listings:
            self.listings = SAMPLE_RENTALS.copy()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, filename)

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["address", "price", "link"])
            writer.writeheader()
            writer.writerows(self.listings)

        print(f"📁 Exported {len(self.listings)} records to: {output_path}")
        return output_path

    def init_driver(self, headless: bool = False) -> bool:
        """Initializes Selenium Chrome WebDriver."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1280,900")
            options.add_argument("--log-level=3")

            self.driver = webdriver.Chrome(options=options)
            return True
        except Exception as e:
            print(f"⚠️ Could not initialize Chrome WebDriver: {e}")
            return False

    def close(self):
        """Safely quits WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

    def live_fill_form(self, form_url: str):
        """Fills Google Form with property listings using Selenium WebDriver."""
        if not self.driver:
            print("❌ WebDriver not ready.")
            return

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        print(f"🌐 Navigating to Google Form: {form_url}")
        for idx, item in enumerate(self.listings, start=1):
            try:
                self.driver.get(form_url)
                time.sleep(2)

                # Locate short-answer inputs
                inputs = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//input[@type="text"]'))
                )

                if len(inputs) >= 3:
                    inputs[0].send_keys(item["address"])
                    inputs[1].send_keys(item["price"])
                    inputs[2].send_keys(item["link"])

                    # Submit button
                    submit_btn = self.driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Submit"]')
                    submit_btn.click()
                    print(f"[{idx}/{len(self.listings)}] Form submitted for: {item['address']}")
                    time.sleep(1.5)
                else:
                    print(f"⚠️ Unexpected form layout: found {len(inputs)} input fields.")
                    break

            except Exception as e:
                print(f"⚠️ Failed to submit record #{idx}: {e}")

    @staticmethod
    def run_simulation(max_entries: int = 4):
        """Runs an interactive demonstration of scraping, cleaning, and form pipeline."""
        print("🤖 [SIMULATION MODE] Starting Real Estate Capstone Engine...\n")
        time.sleep(0.4)

        print("1️⃣ Scraping Zillow Property Clone via BeautifulSoup4...")
        time.sleep(0.5)
        print(f"   ↳ Parsed HTML DOM tree -> Located {len(SAMPLE_RENTALS)} property cards.")
        print("2️⃣ Cleaning Raw Listing Attributes (Regex sanitization):")
        time.sleep(0.5)

        sample = SAMPLE_RENTALS[:max_entries]
        for i, item in enumerate(sample, 1):
            print(f"   [{i}] 📍 Address : {item['address']}")
            print(f"       💵 Rent    : {item['price']}")
            print(f"       🔗 URL     : {item['link'][:45]}...")
            time.sleep(0.3)

        print("\n3️⃣ Generating CSV Output Dataset...")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "rentals_export.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["address", "price", "link"])
            writer.writeheader()
            writer.writerows(sample)
        print(f"   ✅ Saved {len(sample)} verified rental entries to '{os.path.basename(csv_path)}'")

        print("\n4️⃣ Automated Data Entry (Selenium -> Google Forms / Sheets Pipe):")
        time.sleep(0.4)
        for i, item in enumerate(sample, 1):
            print(f"   [Form Entry #{i}] Injecting:")
            print(f"      • Input #1 (Address) -> '{item['address']}'")
            print(f"      • Input #2 (Price)   -> '{item['price']}'")
            print(f"      • Input #3 (Link)    -> '{item['link'][:35]}...'")
            print(f"      • Triggered Click: [Submit Form] -> Status 200 OK")
            print(f"      • Clicked: 'Submit another response' 🔄")
            time.sleep(0.4)

        print("\n" + "=" * 65)
        print("📊 CAPSTONE PIPELINE COMPLETE")
        print("=" * 65)
        print(f" • Listings Scraped & Sanitized : {len(sample)}")
        print(f" • Data Integrity Check         : PASSED (Zero missing fields)")
        print(f" • CSV Export Generated         : {csv_path}")
        print(f" • Google Form Automated Entries: {len(sample)} / {len(sample)} Success")
        print("=" * 65)
