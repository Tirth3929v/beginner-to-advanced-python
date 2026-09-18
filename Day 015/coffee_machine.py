import sys
from art import logo, coffee_cup
from coffee_data import MENU, INITIAL_RESOURCES, RUPEE_DENOMINATIONS

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Global Machine State initialized from coffee_data
profit = 0.0
resources = INITIAL_RESOURCES.copy()


def print_report():
    """Print the current resource values and profit in the coffee machine."""
    print("\n" + "═" * 45)
    print("      📊 DIGITAL COFFEE MACHINE REPORT 📊")
    print("═" * 45)
    print(f"💧 Water  : {resources['water']}ml")
    print(f"🥛 Milk   : {resources['milk']}ml")
    print(f"☕ Coffee : {resources['coffee']}g")
    print(f"💰 Money  : ₹{profit:.2f}")
    print("═" * 45 + "\n")


def is_resource_sufficient(order_ingredients):
    """Returns True when order can be made, False if ingredients are insufficient."""
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"\n❌ Sorry, there is not enough {item}. 😔")
            return False
    return True


def get_valid_note_count(denomination_name):
    """Safely prompt the user for note/coin count, handling non-integer input."""
    while True:
        try:
            count = input(f"   How many {denomination_name}? : ").strip()
            if count == "":
                return 0
            val = int(count)
            if val < 0:
                print("   ⚠️ Please enter a positive number.")
                continue
            return val
        except ValueError:
            print("   ⚠️ Invalid input! Please enter a valid integer count.")


def process_rupees():
    """Returns the total cash calculated from rupees inserted by the user."""
    print("\n💵 Please insert cash / coins (in ₹):")
    rs_50 = get_valid_note_count("₹50 notes")
    rs_20 = get_valid_note_count("₹20 notes")
    rs_10 = get_valid_note_count("₹10 notes/coins")
    rs_5 = get_valid_note_count("₹5 coins")
    
    total = (rs_50 * RUPEE_DENOMINATIONS["rs_50"]) + \
            (rs_20 * RUPEE_DENOMINATIONS["rs_20"]) + \
            (rs_10 * RUPEE_DENOMINATIONS["rs_10"]) + \
            (rs_5 * RUPEE_DENOMINATIONS["rs_5"])
    return total


def is_transaction_successful(money_received, drink_cost):
    """Return True when the payment is accepted, or False if money is insufficient."""
    global profit
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        if change > 0:
            print(f"\n💵 Here is ₹{change:.2f} in change.")
        profit += drink_cost
        return True
    else:
        print(f"\n❌ Sorry, ₹{money_received:.2f} is not enough money for a ₹{drink_cost:.2f} drink. Money refunded.")
        return False


def make_coffee(drink_name, order_ingredients):
    """Deduct the required ingredients from the resources and serve coffee."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"\n☕ Brewing your fresh {drink_name.capitalize()}...")
    print(coffee_cup)
    print(f"✨ Here is your fresh {drink_name.capitalize()} ☕. Enjoy! Have a great day! ✨\n")


def refill_resources():
    """Refill the coffee machine resources to maximum capacity."""
    global resources
    resources["water"] = 500
    resources["milk"] = 500
    resources["coffee"] = 200
    print("\n🔄 Resources successfully refilled to maximum capacity! 🔋")
    print_report()


def coffee_machine():
    """Main Coffee Machine loop handling user operations."""
    print(logo)
    print("Welcome to the Premium Automated Indian Coffee Barista! ☕🇮🇳")
    
    is_on = True
    while is_on:
        print("─" * 50)
        print("Menu Options:")
        print(f" 1. ☕ Espresso    - ₹{MENU['espresso']['cost']}")
        print(f" 2. 🥛 Latte       - ₹{MENU['latte']['cost']}")
        print(f" 3. 🍦 Cappuccino  - ₹{MENU['cappuccino']['cost']}")
        print(" (Commands: 'report' | 'refill' | 'off')")
        
        choice = input("\n👉 What would you like? (espresso/latte/cappuccino): ").strip().lower()

        if choice == "off":
            is_on = False
            print("\n🔌 Shutting down Coffee Machine... Goodbye! 👋\n")
        elif choice == "report":
            print_report()
        elif choice == "refill":
            refill_resources()
        elif choice in MENU:
            drink = MENU[choice]
            print(f"\n You selected: {choice.capitalize()} (₹{drink['cost']})")
            if is_resource_sufficient(drink["ingredients"]):
                payment = process_rupees()
                if is_transaction_successful(payment, drink["cost"]):
                    make_coffee(choice, drink["ingredients"])
        else:
            print(f"\n⚠️ Invalid selection: '{choice}'. Please choose espresso, latte, cappuccino, report, or off.")


if __name__ == "__main__":
    coffee_machine()
