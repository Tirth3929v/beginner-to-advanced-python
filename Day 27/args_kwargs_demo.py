import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def add(*args: float) -> float:
    """Demonstrates *args (arbitrary positional arguments packed into a tuple)."""
    print(f"   Positional args received as tuple: {args}")
    total = sum(args)
    return total


def calculate(n: int, **kwargs) -> int:
    """Demonstrates **kwargs (arbitrary keyword arguments packed into a dictionary)."""
    print(f"   Keyword args received as dict: {kwargs}")
    # kwargs.get() provides safe lookup with default fallback
    n += kwargs.get("add", 0)
    n *= kwargs.get("multiply", 1)
    return n


class Car:
    """Demonstrates optional class configuration using **kwargs like Tkinter widgets."""

    def __init__(self, **kw):
        self.make = kw.get("make", "Generic")
        self.model = kw.get("model", "Sedan")
        self.color = kw.get("color", "Silver")
        self.seats = kw.get("seats", 5)

    def __repr__(self):
        return f"<Car: {self.color} {self.make} {self.model} ({self.seats} seats)>"


def run_args_kwargs_demos():
    """Runs interactive demonstrations of *args and **kwargs in Python."""
    print("\n⚙️  Understanding Python *args and **kwargs")
    print("═" * 60)

    print("1️⃣ Arbitrary Positional Arguments (*args):")
    result1 = add(3, 5, 8, 12, 20)
    print(f"   add(3, 5, 8, 12, 20) -> Sum = {result1}\n")

    print("2️⃣ Arbitrary Keyword Arguments (**kwargs):")
    result2 = calculate(2, add=3, multiply=5)
    print(f"   calculate(2, add=3, multiply=5) -> ((2 + 3) * 5) = {result2}\n")

    print("3️⃣ Tkinter-Style Widget Configuration via **kwargs:")
    my_car = Car(make="Tesla", model="Model S", color="Deep Red")
    print(f"   Car(make='Tesla', model='Model S', color='Deep Red') ->")
    print(f"   {my_car}")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    try:
        run_args_kwargs_demos()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")
