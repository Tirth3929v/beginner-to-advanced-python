class MenuItem:
    """Models each individual drink order item available in the coffee machine."""

    def __init__(self, name: str, water: int, milk: int, coffee: int, cost: float):
        self.name = name
        self.water = water
        self.milk = milk
        self.coffee = coffee
        self.cost = cost

    def __repr__(self) -> str:
        return f"<MenuItem: {self.name.capitalize()} - ₹{self.cost}>"


class Menu:
    """Models the menu of drinks and handles item discovery."""

    def __init__(self):
        self.menu = [
            MenuItem(name="espresso", water=50, milk=0, coffee=18, cost=100.0),
            MenuItem(name="latte", water=200, milk=150, coffee=24, cost=150.0),
            MenuItem(name="cappuccino", water=250, milk=100, coffee=24, cost=180.0),
        ]

    def get_items(self) -> str:
        """Returns all the names of available menu items as a formatted string."""
        options = ""
        for item in self.menu:
            options += f"{item.name}/"
        return options.strip("/")

    def find_drink(self, order_name: str) -> MenuItem | None:
        """Searches the menu for a particular drink by name. Returns the item if found, else None."""
        for item in self.menu:
            if item.name.lower() == order_name.strip().lower():
                return item
        return None
