import sys
from art import logo
from coffee_maker import CoffeeMaker
from menu import Menu
from money_machine import MoneyMachine

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main function orchestrating the OOP Coffee Machine."""
    print(logo)
    print("Welcome to the Object-Oriented Coffee Machine Barista! ☕🤖\n")

    # Instantiate object models
    menu = Menu()
    coffee_maker = CoffeeMaker()
    money_machine = MoneyMachine()

    is_on = True
    while is_on:
        options = menu.get_items()
        print("─" * 50)
        print("Available Commands: 'report' | 'refill' | 'off'")
        user_choice = input(f"👉 What would you like? ({options}): ").strip().lower()

        if user_choice == "off":
            is_on = False
            print("\n🔌 Turning off the Coffee Machine. Goodbye! 👋\n")
        elif user_choice == "report":
            coffee_maker.report()
            money_machine.report()
            print()
        elif user_choice == "refill":
            coffee_maker.refill()
        else:
            drink = menu.find_drink(user_choice)
            if drink is None:
                print(f"\n⚠️ Sorry, '{user_choice}' is not available. Please choose from: {options}")
            else:
                print(f"\n Selected: {drink.name.capitalize()} (₹{drink.cost:.2f})")
                if coffee_maker.is_resource_sufficient(drink):
                    if money_machine.make_payment(drink.cost):
                        coffee_maker.make_coffee(drink)


if __name__ == "__main__":
    main()
