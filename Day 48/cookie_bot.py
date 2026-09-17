"""
Day 48 - Automated Cookie Clicker Game Bot
Demonstrates Selenium WebDriver, element finding by ID, Class, and XPath,
rapid interaction loops, and state-based AI purchase decisions.
Includes a high-speed terminal game simulation engine for instant testing.
"""

import sys
import time

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

COOKIE_GAME_URL = "http://orteil.dashnet.org/experiments/cookie/"


def run_selenium_bot(duration_seconds: int = 60):
    """
    Launches Chrome via Selenium WebDriver, clicks the cookie repeatedly,
    and upgrades store items every 5 seconds.
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
    except ImportError:
        print("⚠️ Selenium is not installed in this environment.")
        print("Launching the high-speed Terminal Game Bot simulation instead!\n")
        run_terminal_bot_simulation(duration_seconds)
        return

    print("\n🌐 Launching Chrome WebDriver for Cookie Clicker...")
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get(COOKIE_GAME_URL)

        cookie = driver.find_element(By.ID, "cookie")
        items = driver.find_elements(By.CSS_SELECTOR, "#store div")
        item_ids = [item.get_attribute("id") for item in items]

        check_interval = 5  # seconds
        timeout = time.time() + check_interval
        bot_end_time = time.time() + duration_seconds

        print(f"🤖 Bot active! Clicking at maximum speed for {duration_seconds} seconds...")

        while time.time() < bot_end_time:
            cookie.click()

            # Every 5 seconds: check prices and buy most expensive affordable upgrade
            if time.time() > timeout:
                all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
                item_prices = []

                for price in all_prices:
                    element_text = price.text
                    if element_text != "":
                        cost = int(element_text.split("-")[1].strip().replace(",", ""))
                        item_prices.append(cost)

                cookie_upgrades = {}
                for n in range(len(item_prices)):
                    cookie_upgrades[item_prices[n]] = item_ids[n]

                money_element = driver.find_element(By.ID, "money").text
                if "," in money_element:
                    money_element = money_element.replace(",", "")
                cookie_count = int(money_element)

                affordable_upgrades = {cost: id_ for cost, id_ in cookie_upgrades.items() if cookie_count >= cost}

                if affordable_upgrades:
                    highest_affordable = max(affordable_upgrades)
                    to_purchase_id = affordable_upgrades[highest_affordable]
                    driver.find_element(By.ID, to_purchase_id).click()
                    print(f"🛒 Purchased Upgrade: {to_purchase_id} for {highest_affordable} cookies!")

                timeout = time.time() + check_interval

        cps = driver.find_element(By.ID, "cps").text
        print(f"\n🏆 Final Result: Cookies per second: {cps}")
        driver.quit()

    except Exception as e:
        print(f"ℹ️ Browser automation note: {e}")
        print("Falling back to local terminal bot engine...")
        run_terminal_bot_simulation(duration_seconds)


def run_terminal_bot_simulation(seconds: int = 15):
    """
    Terminal Cookie Clicker Engine & Bot Simulation.
    Demonstrates the exact algorithm: rapid clicking, passive CPS generation,
    and buying the most expensive available upgrades every 3-5 seconds.
    """
    print("\n" + "=" * 65)
    print(" 🍪 TERMINAL COOKIE CLICKER BOT ENGINE SIMULATION")
    print("=" * 65)

    cookies = 0
    cps = 0.0  # Cookies Per Second
    click_power = 1

    # Store items: (Name, Base Cost, CPS boost)
    store = [
        {"name": "Cursor", "cost": 15, "cps": 0.5, "count": 0},
        {"name": "Grandma", "cost": 100, "cps": 4.0, "count": 0},
        {"name": "Factory", "cost": 500, "cps": 32.0, "count": 0},
        {"name": "Mine", "cost": 2000, "cps": 150.0, "count": 0}
    ]

    start = time.time()
    last_upgrade_check = time.time()
    clicks_performed = 0

    try:
        while time.time() - start < seconds:
            # Bot click action
            cookies += click_power
            clicks_performed += 1

            # Passive CPS accumulation
            time.sleep(0.05)
            cookies += (cps * 0.05)

            # Check store upgrades every 2.5 seconds
            if time.time() - last_upgrade_check >= 2.5:
                # Find most expensive affordable upgrade
                affordable = [item for item in store if cookies >= item["cost"]]
                if affordable:
                    best_item = max(affordable, key=lambda x: x["cost"])
                    cookies -= best_item["cost"]
                    best_item["count"] += 1
                    best_item["cost"] = int(best_item["cost"] * 1.15)
                    cps += best_item["cps"]
                    elapsed = round(time.time() - start, 1)
                    print(f" [{elapsed:4.1f}s] 🛒 Bought: {best_item['name']}! (CPS now: {cps:.1f}/s | Bank: {int(cookies):,})")

                last_upgrade_check = time.time()

        print("=" * 65)
        print(f" ⏱️ Bot Duration: {seconds}s")
        print(f" 👆 Clicks Executed: {clicks_performed:,}")
        print(f" 🍪 Final Cookie Bank: {int(cookies):,}")
        print(f" ⚡ Final Cookies Per Second (CPS): {cps:.1f}/s")
        print(" 🏭 Purchased Inventory:")
        for item in store:
            print(f"    • {item['name']:10s}: {item['count']:2d} owned")
        print("=" * 65 + "\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Simulation stopped.\n")
