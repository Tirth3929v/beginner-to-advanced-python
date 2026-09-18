"""
Day 51: Internet Speed Twitter Complaint Bot Engine
Measures broadband bandwidth via Speedtest and automatically tweets complaints
to ISP handles when actual speeds fall below promised contractual limits.
Includes full live Selenium WebDriver driver + offline simulation mode.
"""

import sys
import os
import time
import random
from typing import Tuple, Dict, Any

# Unicode safe console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class InternetSpeedTwitterBot:
    """
    Automated watchdog for monitoring ISP network bandwidth and broadcasting
    tweets on Twitter/X via Selenium automation when service drops below SLA.
    """

    def __init__(
        self,
        promised_down: float = 150.0,
        promised_up: float = 25.0,
        isp_handle: str = "InternetProvider",
        twitter_user: str = "",
        twitter_pass: str = "",
        headless: bool = False,
    ):
        self.promised_down = promised_down
        self.promised_up = promised_up
        self.isp_handle = isp_handle
        self.twitter_user = twitter_user or os.environ.get("TWITTER_EMAIL", "your_twitter_email")
        self.twitter_pass = twitter_pass or os.environ.get("TWITTER_PASSWORD", "your_twitter_password")
        self.headless = headless
        self.down = 0.0
        self.up = 0.0
        self.ping = 0.0
        self.driver = None

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

    def live_get_internet_speed(self) -> Tuple[float, float]:
        """Runs a live speedtest on speedtest.net using Selenium."""
        if not self.driver:
            print("❌ WebDriver not ready.")
            return 0.0, 0.0

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        print("🌐 Navigating to https://www.speedtest.net ...")
        self.driver.get("https://www.speedtest.net")
        time.sleep(3)

        try:
            # Dismiss cookie banner if present
            try:
                consent_btn = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
                consent_btn.click()
                time.sleep(1)
            except Exception:
                pass

            # Click the start Go button
            print("⚡ Starting speed test probe...")
            go_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "js-start-test"))
            )
            go_button.click()

            print("⏳ Testing network latency and throughput (approx 45s)...")
            # Wait until download and upload metrics display
            time.sleep(45)

            down_elem = self.driver.find_element(By.CLASS_NAME, "download-speed")
            up_elem = self.driver.find_element(By.CLASS_NAME, "upload-speed")

            self.down = float(down_elem.text.strip())
            self.up = float(up_elem.text.strip())
            print(f"✅ Measured Speeds: Down: {self.down} Mbps | Up: {self.up} Mbps")
            return self.down, self.up

        except Exception as e:
            print(f"⚠️ Speedtest execution failed: {e}")
            return 0.0, 0.0

    def live_tweet_at_provider(self) -> bool:
        """Publishes complaint tweet via Selenium automation on Twitter/X."""
        if not self.driver:
            print("❌ WebDriver not ready.")
            return False

        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        message = (
            f"Hey @{self.isp_handle}, why is my internet speed {self.down:.1f} Mbps down / "
            f"{self.up:.1f} Mbps up when I pay for {self.promised_down:.0f} Mbps down / "
            f"{self.promised_up:.0f} Mbps up? @ConsumerAffairs #NetNeutrality #SpeedtestBot"
        )

        print("🐦 Navigating to https://twitter.com/login ...")
        self.driver.get("https://twitter.com/login")
        time.sleep(4)

        try:
            # Enter username/email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            email_field.send_keys(self.twitter_user)
            email_field.send_keys(Keys.ENTER)
            time.sleep(2)

            # Enter password
            pass_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            pass_field.send_keys(self.twitter_pass)
            pass_field.send_keys(Keys.ENTER)
            time.sleep(4)

            # Locate tweet composing box
            tweet_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetTextarea_0"]'))
            )
            tweet_box.send_keys(message)
            time.sleep(1)

            # Click tweet button
            tweet_btn = self.driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
            tweet_btn.click()
            print(f"🚀 Complaint tweet posted successfully!\nPayload: \"{message}\"")
            return True

        except Exception as e:
            print(f"⚠️ Twitter login / posting interaction failed: {e}")
            return False

    def simulate_test(self, force_throttle: bool = True):
        """Simulates broadband testing and automated ISP complaint dispatch."""
        print("🔍 [SIMULATION MODE] Starting Automated Speedtest Watchdog...\n")
        time.sleep(0.4)

        print(f"📋 Contractual SLA Thresholds:")
        print(f"   • Promised Download : {self.promised_down:.1f} Mbps")
        print(f"   • Promised Upload   : {self.promised_up:.1f} Mbps")
        print(f"   • Target ISP Handle : @{self.isp_handle}\n")

        print("📡 Connecting to nearest Ookla edge test server...")
        time.sleep(0.6)
        self.ping = round(random.uniform(12.0, 38.0), 1)
        print(f"   ↳ Latency (Ping): {self.ping} ms [STABLE]")

        time.sleep(0.6)
        if force_throttle:
            # Drop below SLA
            self.down = round(random.uniform(28.0, 52.0), 2)
            self.up = round(random.uniform(4.5, 9.2), 2)
        else:
            self.down = round(random.uniform(self.promised_down * 0.95, self.promised_down * 1.1), 2)
            self.up = round(random.uniform(self.promised_up * 0.95, self.promised_up * 1.1), 2)

        print(f"   ↳ Measured Download : {self.down} Mbps")
        time.sleep(0.5)
        print(f"   ↳ Measured Upload   : {self.up} Mbps\n")
        time.sleep(0.5)

        # Evaluate against SLA
        down_deficient = self.down < self.promised_down
        up_deficient = self.up < self.promised_up

        print("=" * 60)
        print("📊 SLA EVALUATION REPORT")
        print("=" * 60)
        print(f" • Download Status : {'❌ DEFICIENT (Throttled)' if down_deficient else '✅ ACCEPTABLE'}")
        print(f"   Deficit: {self.promised_down - self.down:.1f} Mbps (-{((self.promised_down - self.down)/self.promised_down)*100:.1f}%)")
        print(f" • Upload Status   : {'❌ DEFICIENT (Throttled)' if up_deficient else '✅ ACCEPTABLE'}")
        print(f"   Deficit: {self.promised_up - self.up:.1f} Mbps (-{((self.promised_up - self.up)/self.promised_up)*100:.1f}%)")
        print("=" * 60)

        if down_deficient or up_deficient:
            print("\n🚨 SLA BREACH DETECTED! Initiating Twitter/X Automation Bot...")
            time.sleep(0.6)
            tweet_text = (
                f"Hey @{self.isp_handle}, why is my internet speed {self.down} Mbps down / "
                f"{self.up} Mbps up when I pay for {self.promised_down:.0f} Mbps down / "
                f"{self.promised_up:.0f} Mbps up? @ConsumerAffairs #NetNeutrality #SpeedtestBot"
            )
            print("\n🐦 [COMPOSED TWEET PAYLOAD]:")
            print(f"   \"{tweet_text}\"\n")
            time.sleep(0.5)
            print("   [1] Initialized Twitter authentication flow...")
            time.sleep(0.4)
            print("   [2] Navigated to tweet composer...")
            time.sleep(0.4)
            print("   [3] Filled textarea payload via Selenium ActionChains...")
            time.sleep(0.4)
            print("   [4] Clicked [Post Tweet] button -> Status HTTP 200 OK ✨")
            print("\n✅ Automated complaint logged to ISP public feed.")
        else:
            print("\n🎉 Connection speeds meet contract specifications. No tweet needed.")
