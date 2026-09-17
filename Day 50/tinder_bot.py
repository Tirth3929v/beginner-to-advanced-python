"""
Day 50: Tinder Automated Swiping Bot Engine
Implements Selenium WebDriver automation for web-based dating profiles,
handling modal dialogs, cookie banners, match popups, and automated swipe loops.
Includes dual-mode operation (Live Chrome WebDriver + Interactive Terminal Simulation).
"""

import sys
import os
import time
import random
from typing import Dict, Any, List

# Unicode safe console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SAMPLE_PROFILES = [
    {"name": "Sophia", "age": 24, "bio": "Software engineer & coffee enthusiast ☕ Code, hike, repeat.", "dist": "3 miles away"},
    {"name": "Marcus", "age": 27, "bio": "Architectural designer 📐 Loves photography and indie concerts 🎸", "dist": "5 miles away"},
    {"name": "Elena", "age": 23, "bio": "Bioinformatics student 🧬 Dog mom to a golden retriever 🐕", "dist": "2 miles away"},
    {"name": "David", "age": 26, "bio": "Fintech founder 🚀 Looking for someone to explore rooftop cafes with.", "dist": "7 miles away"},
    {"name": "Aria", "age": 25, "bio": "Travel photographer 📸 Currently learning Spanish and surfing 🏄‍♀️", "dist": "4 miles away"},
    {"name": "Lucas", "age": 28, "bio": "Data Scientist & marathon runner 🏃 Always looking for good book recs 📚", "dist": "6 miles away"},
]


class TinderBot:
    """
    Automated browser bot for navigating Tinder Web using Selenium WebDriver.
    """

    def __init__(self, email: str = "", password: str = "", headless: bool = False):
        self.email = email
        self.password = password
        self.headless = headless
        self.driver = None
        self.swipes_right = 0
        self.swipes_left = 0
        self.matches_found = 0

    def init_driver(self) -> bool:
        """Initializes the Chrome WebDriver."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options

            options = Options()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280,900")
            options.add_argument("--log-level=3")

            self.driver = webdriver.Chrome(options=options)
            return True
        except Exception as e:
            print(f"⚠️ Could not initialize Chrome WebDriver: {e}")
            return False

    def close(self):
        """Closes the active WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

    def live_auto_swipe(self, target_swipes: int = 10):
        """Executes automated swiping on live Tinder session."""
        if not self.driver:
            print("❌ Chrome WebDriver is not initialized.")
            return

        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import (
            NoSuchElementException,
            ElementClickInterceptedException,
            TimeoutException,
        )

        print(f"🌐 Navigating to https://tinder.com ...")
        self.driver.get("https://tinder.com")
        time.sleep(3)

        print("ℹ️ Please ensure you are logged into Tinder in the opened browser window.")
        print("Waiting 15 seconds for profile feed to load...")
        time.sleep(15)

        for i in range(1, target_swipes + 1):
            try:
                # Swipe right using ArrowRight key on the body element
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ARROW_RIGHT)
                self.swipes_right += 1
                print(f"[{i}/{target_swipes}] 👉 Swiped RIGHT!")
                time.sleep(random.uniform(1.2, 2.5))

            except ElementClickInterceptedException:
                print("⚠️ Modal detected (Match popup / App download prompt). Attempting dismiss...")
                try:
                    dismiss_btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "Not interested") or contains(text(), "Maybe Later")]')
                    dismiss_btn.click()
                    self.matches_found += 1
                    print("🎉 Dismissed match popup! Continuing...")
                except NoSuchElementException:
                    try:
                        body = self.driver.find_element(By.TAG_NAME, "body")
                        body.send_keys(Keys.ESCAPE)
                    except Exception:
                        pass
                time.sleep(1.5)

            except Exception as e:
                print(f"⚠️ Encountered navigation interruption: {e}")
                time.sleep(2)

        print("\n🏁 Swiping session completed!")
        print(f"📊 Total Rights: {self.swipes_right} | Matches Recorded: {self.matches_found}")

    @staticmethod
    def run_simulation(swipe_count: int = 8):
        """Runs a visual terminal simulation demonstrating the bot logic."""
        print("🤖 [SIMULATION MODE] Starting Automated Swiper Engine...\n")
        time.sleep(0.5)

        print("1️⃣ Initializing Headless Chrome WebDriver...")
        time.sleep(0.5)
        print("2️⃣ Navigating to https://tinder.com")
        time.sleep(0.5)
        print("3️⃣ Handling Initial Geolocation & Notification Permissions [Allow]")
        time.sleep(0.5)
        print("4️⃣ Accepting GDPR / Essential Cookie Preferences [Dismissed]\n")
        time.sleep(0.5)

        rights = 0
        lefts = 0
        matches = 0

        for i in range(1, swipe_count + 1):
            profile = SAMPLE_PROFILES[(i - 1) % len(SAMPLE_PROFILES)]
            print("-" * 60)
            print(f"👤 Candidate #{i}: {profile['name']}, {profile['age']} ({profile['dist']})")
            print(f"   💬 Bio: \"{profile['bio']}\"")

            # Determine swipe action (85% right, 15% left)
            swipe_choice = "RIGHT" if random.random() < 0.85 else "LEFT"
            time.sleep(0.7)

            if swipe_choice == "RIGHT":
                rights += 1
                print(f"   👉 Decision: Swiping RIGHT (Keyboard: ARROW_RIGHT)")
                # Simulate match chance (25%)
                if random.random() < 0.25:
                    matches += 1
                    time.sleep(0.4)
                    print(f"   🎉 IT'S A MATCH! You and {profile['name']} liked each other!")
                    print("   🔔 Handling popup: Clicked 'Keep Swiping' modal button.")
            else:
                lefts += 1
                print(f"   👈 Decision: Swiping LEFT (Keyboard: ARROW_LEFT)")

            time.sleep(0.4)

        print("\n" + "=" * 60)
        print("📊 SESSION SUMMARY & ANALYTICS")
        print("=" * 60)
        print(f" • Total Profiles Evaluated : {swipe_count}")
        print(f" • Swiped Right (Liked)    : {rights} ({rights / swipe_count * 100:.1f}%)")
        print(f" • Swiped Left (Passed)    : {lefts} ({lefts / swipe_count * 100:.1f}%)")
        print(f" • New Matches Unlocked    : {matches}")
        print("=" * 60)
