"""
Day 48 - Selenium Webdriver & Cookie Clicker Bot Studio
Main launcher to run browser automation or high-speed terminal game simulation.
"""

import sys
from art import logo
from cookie_bot import (
    run_selenium_bot,
    run_terminal_bot_simulation,
)

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def explain_selenium_locators():
    """Prints a reference guide to Selenium 4 element locators."""
    print("\n" + "=" * 70)
    print(" 🤖 SELENIUM WEBDRIVER 4 ELEMENT LOCATORS CHEAT SHEET")
    print("=" * 70)
    print("""
 In modern Selenium 4:
   from selenium.webdriver.common.by import By

 1. By.ID:
    driver.find_element(By.ID, "cookie")

 2. By.CLASS_NAME:
    driver.find_element(By.CLASS_NAME, "price")

 3. By.NAME:
    driver.find_element(By.NAME, "search_query")

 4. By.CSS_SELECTOR:
    driver.find_elements(By.CSS_SELECTOR, "#store div b")

 5. By.XPATH:
    driver.find_element(By.XPATH, '//*[@id="cookie"]')

 6. Actions:
    element.click()
    element.send_keys("Python", Keys.ENTER)
    element.text
    """)
    print("=" * 70 + "\n")


def main():
    print(logo)
    print("Welcome to Day 48 - Selenium WebDriver & Cookie Clicker Studio! 🤖🍪\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. ⚡ Run High-Speed Terminal Bot Simulation (10 seconds)")
            print(" 2. 🌐 Launch Live Selenium Chrome Browser Automation (60 seconds)")
            print(" 3. 📚 View Selenium 4 Locators Cheat Sheet")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                run_terminal_bot_simulation(10)
            elif choice == "2":
                run_selenium_bot(60)
            elif choice == "3":
                explain_selenium_locators()
            elif choice == "4":
                print("\nExiting Day 48 Studio... Happy automating! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-4.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 48 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
