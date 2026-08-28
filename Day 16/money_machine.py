class MoneyMachine:
    """Models the payment processing mechanism and profit ledger for Indian Rupees (₹)."""

    CURRENCY_SYMBOL = "₹"
    DENOMINATIONS = {
        "rs_500": 500,
        "rs_200": 200,
        "rs_100": 100,
        "rs_50": 50,
        "rs_20": 20,
        "rs_10": 10,
        "rs_5": 5,
    }

    def __init__(self):
        self.profit = 0.0
        self.money_received = 0.0

    def report(self) -> None:
        """Prints current profit collected by the money machine."""
        print(f"💰 Total Profit Earned: {self.CURRENCY_SYMBOL}{self.profit:.2f}")

    def prompt_valid_count(self, label: str) -> int:
        """Safely prompts user for note/coin count with error handling."""
        while True:
            try:
                user_input = input(f"   How many {label}? : ").strip()
                if user_input == "":
                    return 0
                val = int(user_input)
                if val < 0:
                    print("   ⚠️ Count cannot be negative. Try again.")
                    continue
                return val
            except ValueError:
                print("   ⚠️ Invalid integer input. Please enter a valid count.")

    def process_coins(self) -> float:
        """Prompts user to insert cash notes/coins and returns total value calculated."""
        print(f"\n💵 Please insert cash / notes ({self.CURRENCY_SYMBOL}):")
        total = 0.0
        total += self.prompt_valid_count("₹500 notes") * 500
        total += self.prompt_valid_count("₹200 notes") * 200
        total += self.prompt_valid_count("₹100 notes") * 100
        total += self.prompt_valid_count("₹50 notes") * 50
        total += self.prompt_valid_count("₹20 notes") * 20
        total += self.prompt_valid_count("₹10 notes/coins") * 10
        total += self.prompt_valid_count("₹5 coins") * 5
        self.money_received = float(total)
        return self.money_received

    def make_payment(self, cost: float) -> bool:
        """Processes payment transaction for cost. Returns True if payment accepted, False otherwise."""
        self.process_coins()
        if self.money_received >= cost:
            change = round(self.money_received - cost, 2)
            if change > 0:
                print(f"\n💵 Here is {self.CURRENCY_SYMBOL}{change:.2f} in change.")
            self.profit += cost
            self.money_received = 0.0
            return True
        else:
            print(f"\n❌ Sorry, {self.CURRENCY_SYMBOL}{self.money_received:.2f} is not enough. "
                  f"Item costs {self.CURRENCY_SYMBOL}{cost:.2f}. Money refunded.")
            self.money_received = 0.0
            return False
