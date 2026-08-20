import os
from art import farewell, logo


def add(n1, n2):
    return n1 + n2


def subtract(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    if n2 == 0:
        return "ERROR: Division by zero is undefined in standard universe physics! 💥"
    return n1 / n2


operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

descriptors = {
    "+": "➕ Adding values...",
    "-": "➖ Subtracting values...",
    "*": "✖️ Multiplying values...",
    "/": "➗ Dividing values...",
}


def get_float_input(prompt):
    """Helper function to safely get float input from user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("⚠️ Invalid input! Please enter a valid numerical value (e.g. 42 or 3.14).\n")


def calculate():
    print(logo)
    print("✨ Welcome to PyCalc Engine! Let's power through some math.\n")

    num1 = get_float_input("👉 Enter the initial number: ")
    should_accumulate = True

    while should_accumulate:
        print("\nAvailable Operations:")
        print("  [ + ] Addition      [ - ] Subtraction")
        print("  [ * ] Multiplication [ / ] Division")

        operation_symbol = input("\n👉 Pick an operation symbol (+, -, *, /): ").strip()

        if operation_symbol not in operations:
            print(f"❌ '{operation_symbol}' is not a valid operation. Try again!")
            continue

        num2 = get_float_input("👉 Enter the next number: ")

        print(f"\n⚡ {descriptors[operation_symbol]}")
        answer = operations[operation_symbol](num1, num2)

        print("\n" + "═" * 60)
        if isinstance(answer, (int, float)):
            # Format nicely if integer float
            formatted_ans = int(answer) if answer.is_integer() else round(answer, 4)
            formatted_n1 = int(num1) if num1.is_integer() else round(num1, 4)
            formatted_n2 = int(num2) if num2.is_integer() else round(num2, 4)
            print(f"🎯 RESULT: {formatted_n1} {operation_symbol} {formatted_n2} = {formatted_ans}")
        else:
            print(f"🎯 RESULT: {answer}")
        print("═" * 60 + "\n")

        print("What would you like to do next?")
        print("  [ y ] Continue calculating with this result")
        print("  [ n ] Clear memory and start a brand new calculation")
        print("  [ q ] Quit calculator")

        choice = input("\n👉 Choice (y/n/q): ").lower().strip()

        if choice == "y":
            if isinstance(answer, (int, float)):
                num1 = answer
                print(f"\n🧠 Memory updated! Continuing with baseline: {num1}")
            else:
                print("\n⚠️ Cannot chain calculations from an error state. Restarting...\n")
                should_accumulate = False
                calculate()
        elif choice == "n":
            should_accumulate = False
            print("\n" * 2)
            print("🧹 Memory matrix cleared! Starting fresh calculation...\n")
            calculate()
        elif choice == "q":
            should_accumulate = False
            print(farewell)
        else:
            print("\n⚠️ Unrecognized option. Starting new calculation for safety.\n")
            should_accumulate = False
            calculate()


if __name__ == "__main__":
    calculate()
