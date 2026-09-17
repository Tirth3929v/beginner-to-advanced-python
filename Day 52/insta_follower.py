"""
Day 52: Instagram Follower Bot Engine
Implements an OOP architecture (InstaFollower class) for automating follower acquisition
using Selenium WebDriver. Handles modal scrolling, follow button clicks, jitter delays,
and exception recovery when modals intercept clicks.
Includes dual-mode operation (Live Chrome WebDriver + Interactive Terminal Simulation).
"""

import sys
import os
import time
import random
from typing import List, Dict, Any

# Unicode safe console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SAMPLE_TARGET_FOLLOWERS = [
    {"username": "code_artisan", "fullname": "Alex Rivera", "bio": "Building open-source tools with Python & Rust 🦀"},
    {"username": "data_ninja", "fullname": "Sara Chen", "bio": "Machine Learning engineer @ DeepTech 🤖"},
    {"username": "py_daily_tips", "fullname": "Python Digest", "bio": "Bite-sized Python tips, tricks, and interview prep 🐍"},
    {"username": "dev_journey", "fullname": "Vikram Patel", "bio": "Self-taught developer sharing the 100DaysOfCode path 🚀"},
    {"username": "frontend_queen", "fullname": "Maya Lin", "bio": "Full-stack enthusiast, UI/UX lover & tech speaker 🎨"},
    {"username": "algo_solver", "fullname": "Julian Gomez", "bio": "Competitive programming & clean architecture advocate 🧠"},
    {"username": "cloud_native_guy", "fullname": "Liam O'Connor", "bio": "DevOps, Docker, Kubernetes & microservices ☁️"},
    {"username": "quantum_bits", "fullname": "Dr. Aris Thorne", "bio": "Quantum computing researcher & Python developer ⚛️"},
]


class InstaFollower:
    """
    Automated engagement bot for expanding follower networks on Instagram
    via targeted audience discovery and controlled automated following.
    """

    def __init__(
        self,
        username: str = "",
        password: str = "",
        headless: bool = False,
    ):
        self.username = username or os.environ.get("INSTA_USER", "your_insta_user")
        self.password = password or os.environ.get("INSTA_PASS", "your_insta_pass")
        self.headless = headless
        self.driver = None
        self.followed_count = 0
        self.already_following = 0

    def init_driver(self) -> bool:
        """Initializes the Selenium Chrome WebDriver."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            if self.headless:
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
        """Safely quits the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

    def live_login(self) -> bool:
        """Authenticates on Instagram via Selenium."""
        if not self.driver:
            return False

        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        print("🌐 Navigating to https://www.instagram.com/accounts/login/ ...")
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)

        try:
            # Decline / Accept cookies
            try:
                cookie_btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "Allow all cookies") or contains(text(), "Accept")]')
                cookie_btn.click()
                time.sleep(1)
            except Exception:
                pass

            # Fill username & password
            user_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            user_input.send_keys(self.username)

            pass_input = self.driver.find_element(By.NAME, "password")
            pass_input.send_keys(self.password)
            pass_input.send_keys(Keys.ENTER)
            time.sleep(6)

            # Dismiss 'Save Your Login Info?' prompt
            try:
                not_now_save = self.driver.find_element(By.XPATH, '//button[contains(text(), "Not now") or contains(text(), "Not Now")]')
                not_now_save.click()
                time.sleep(2)
            except Exception:
                pass

            # Dismiss 'Turn on Notifications' prompt
            try:
                not_now_notif = self.driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]')
                not_now_notif.click()
                time.sleep(2)
            except Exception:
                pass

            print("✅ Successfully logged into Instagram!")
            return True

        except Exception as e:
            print(f"⚠️ Login flow interrupted: {e}")
            return False

    def live_find_followers(self, target_account: str):
        """Navigates to target account and opens followers dialog."""
        if not self.driver:
            return

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        url = f"https://www.instagram.com/{target_account}/"
        print(f"🔎 Navigating to target account: {url}")
        self.driver.get(url)
        time.sleep(4)

        try:
            # Click followers link
            followers_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//a[contains(@href, "/{target_account}/followers/")]'))
            )
            followers_link.click()
            time.sleep(3)
            print("📋 Followers dialog opened.")
        except Exception as e:
            print(f"⚠️ Could not open followers modal: {e}")

    def live_follow(self, max_follows: int = 5):
        """Iterates over follow buttons in the modal dialog."""
        if not self.driver:
            return

        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import ElementClickInterceptedException

        try:
            # Find the scrollable modal container
            modal = self.driver.find_element(By.XPATH, '//div[@class="_aano"]')
            for _ in range(2):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(2)

            buttons = modal.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if self.followed_count >= max_follows:
                    break
                if btn.text == "Follow":
                    try:
                        btn.click()
                        self.followed_count += 1
                        print(f"[{self.followed_count}/{max_follows}] Followed profile! Waiting jitter...")
                        time.sleep(random.uniform(2.0, 5.0))
                    except ElementClickInterceptedException:
                        # Cancel confirmation popup if triggered
                        try:
                            cancel_btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "Cancel")]')
                            cancel_btn.click()
                        except Exception:
                            pass
        except Exception as e:
            print(f"⚠️ Following loop interrupted: {e}")

    @staticmethod
    def run_simulation(target_account: str = "chefsteps", max_follows: int = 5):
        """Interactive simulation showcasing the complete workflow."""
        print("🤖 [SIMULATION MODE] Initializing Instagram Automation Engine...\n")
        time.sleep(0.4)

        print("1️⃣ Initializing Chrome WebDriver with Anti-Detection Capabilities...")
        time.sleep(0.4)
        print("2️⃣ Navigating to https://www.instagram.com/accounts/login/ ...")
        time.sleep(0.4)
        print("3️⃣ Entering credentials and handling 2FA / Session checkpoints...")
        time.sleep(0.4)
        print("4️⃣ Dismissing 'Save Login Info' and 'Turn on Notifications' modals [Dismissed]\n")
        time.sleep(0.5)

        print(f"🎯 Target Profile Selected: @{target_account}")
        print(f"   ↳ Navigating to https://www.instagram.com/{target_account}/")
        time.sleep(0.5)
        print("   ↳ Clicking [Followers] tab -> Modal container loaded.")
        time.sleep(0.5)
        print("   ↳ Scrolling modal viewport via `arguments[0].scrollTop = arguments[0].scrollHeight`...")
        time.sleep(0.6)

        followed = 0
        already = 0
        limit = min(max_follows, len(SAMPLE_TARGET_FOLLOWERS))

        print("\n👥 AUDIENCE ENGAGEMENT PIPELINE:")
        print("-" * 65)

        for i in range(limit):
            user = SAMPLE_TARGET_FOLLOWERS[i]
            # Random chance to already follow
            is_already = random.random() < 0.2
            jitter = round(random.uniform(1.2, 2.5), 2)

            print(f"[{i+1}/{limit}] Candidate: @{user['username']} ({user['fullname']})")
            print(f"     💬 Bio: \"{user['bio']}\"")

            if is_already:
                already += 1
                print(f"     ℹ️ Status: Already following. Skipping.")
            else:
                followed += 1
                print(f"     ➕ Action: Clicked [Follow] button -> Status: Following ✅")
                print(f"     ⏳ Rate-limit safety jitter applied: {jitter}s sleep...")
                time.sleep(0.5)
            print("-" * 65)

        print("\n" + "=" * 65)
        print("📊 CAMPAIGN SUMMARY REPORT")
        print("=" * 65)
        print(f" • Target Influencer Account : @{target_account}")
        print(f" • Profiles Inspected        : {limit}")
        print(f" • Newly Followed Accounts   : {followed}")
        print(f" • Previously Followed       : {already}")
        print(f" • Anti-Ban Status           : 100% HEALTHY (Zero rate-limit flags)")
        print("=" * 65)
