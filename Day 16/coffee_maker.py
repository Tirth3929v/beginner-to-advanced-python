from art import coffee_cup
from menu import MenuItem


class CoffeeMaker:
    """Models the physical hardware and resource state of the coffee machine."""

    def __init__(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }

    def report(self) -> None:
        """Prints a formatted report of current machine resources."""
        print("\n" + "═" * 45)
        print("      📊 RESOURCE STATUS REPORT 📊")
        print("═" * 45)
        print(f"💧 Water  : {self.resources['water']}ml")
        print(f"🥛 Milk   : {self.resources['milk']}ml")
        print(f"☕ Coffee : {self.resources['coffee']}g")
        print("═" * 45 + "\n")

    def is_resource_sufficient(self, drink: MenuItem) -> bool:
        """Returns True when order can be made, False if ingredients are insufficient."""
        can_make = True
        for item in self.resources:
            required = getattr(drink, item, 0)
            if required > self.resources[item]:
                print(f"\n❌ Sorry, there is not enough {item}. 😔")
                can_make = False
        return can_make

    def make_coffee(self, order: MenuItem) -> None:
        """Deducts the required ingredients from resources and dispenses coffee."""
        for item in self.resources:
            self.resources[item] -= getattr(order, item, 0)
        print(f"\n☕ Brewing your fresh {order.name.capitalize()}...")
        print(coffee_cup)
        print(f"✨ Here is your fresh {order.name.capitalize()} ☕. Enjoy! Have a great day! ✨\n")

    def refill(self) -> None:
        """Refills machine resources back to standard capacity."""
        self.resources["water"] = 500
        self.resources["milk"] = 500
        self.resources["coffee"] = 200
        print("\n🔄 Resources successfully refilled to maximum capacity! 🔋")
        self.report()
