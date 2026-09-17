"""
Day 54: Python Decorator Playground & Execution Benchmarker
Explores Python higher-order functions, first-class citizen closures,
and custom function wrappers (@speed_calc_decorator, @make_bold, etc.).
"""

import sys
import time
from functools import wraps

# Unicode safe console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def speed_calc_decorator(fn):
    """Decorator measuring precise wall-clock execution time of target function."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = fn(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = (end_time - start_time) * 1000  # in milliseconds
        print(f"⏱️ [{fn.__name__}] executed in: {elapsed:.3f} ms")
        return result
    return wrapper


def make_bold(fn):
    """Wraps returned text in HTML <b> tags."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return f"<b>{fn(*args, **kwargs)}</b>"
    return wrapper


def make_emphasis(fn):
    """Wraps returned text in HTML <em> tags."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return f"<em>{fn(*args, **kwargs)}</em>"
    return wrapper


def make_underlined(fn):
    """Wraps returned text in HTML <u> tags."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return f"<u>{fn(*args, **kwargs)}</u>"
    return wrapper


@speed_calc_decorator
def fast_calculation():
    """Calculates sum of squares for 500,000 integers."""
    return sum(i * i for i in range(500_000))


@speed_calc_decorator
def slow_calculation():
    """Calculates sum of squares for 2,000,000 integers."""
    return sum(i * i for i in range(2_000_000))


@make_bold
@make_emphasis
@make_underlined
def greet(name: str) -> str:
    """Returns styled greeting string."""
    return f"Welcome to Flask & Python Decorators, {name}!"


def run_decorator_demo():
    """Executes interactive demonstrations of decorator concepts."""
    print("=" * 65)
    print(" 🧪 EXERCISE 1: High-Precision Speed Calculation Decorator")
    print("=" * 65)
    print("Benchmarking `fast_calculation()` (500k iterations)...")
    res1 = fast_calculation()
    print(f"Result checksum: {res1:,}\n")

    print("Benchmarking `slow_calculation()` (2M iterations)...")
    res2 = slow_calculation()
    print(f"Result checksum: {res2:,}\n")

    print("=" * 65)
    print(" 🧪 EXERCISE 2: Multi-Layered HTML Tag Wrappers")
    print("=" * 65)
    print("Decorated function: @make_bold -> @make_emphasis -> @make_underlined")
    styled_text = greet("Developer")
    print(f"Raw Output    : {styled_text}")
    print(f"Rendered Look : <b><em><u>Welcome to Flask & Python Decorators, Developer!</u></em></b>\n")
