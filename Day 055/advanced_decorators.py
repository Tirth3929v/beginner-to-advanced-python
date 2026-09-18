"""
Day 55: Advanced Decorators with *args and **kwargs
Implements logging and authentication decorators demonstrating variable-length
positional and keyword argument interception.
"""

from functools import wraps


def logging_decorator(fn):
    """Decorator that logs the function name, arguments, and returned value."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        args_str = ", ".join(map(repr, args))
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        print(f"📝 Calling {fn.__name__}({all_args})...")
        result = fn(*args, **kwargs)
        print(f"   ↳ Returned: {result!r}")
        return result
    return wrapper


class User:
    def __init__(self, name: str, is_logged_in: bool = False):
        self.name = name
        self.is_logged_in = is_logged_in


def is_authenticated_decorator(fn):
    """Decorator ensuring that the user argument is logged in before execution."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = None
        for arg in args:
            if isinstance(arg, User):
                user = arg
                break
        if not user:
            user = kwargs.get("user")

        if user and user.is_logged_in:
            return fn(*args, **kwargs)
        else:
            print(f"⛔ Access Denied: User '{getattr(user, 'name', 'Guest')}' is not authenticated!")
            return None
    return wrapper


@logging_decorator
def multiply_numbers(a: int, b: int, c: int = 1) -> int:
    return a * b * c


@is_authenticated_decorator
def create_blog_post(user: User, title: str) -> str:
    msg = f"Post '{title}' successfully published by {user.name}!"
    print(f"✅ {msg}")
    return msg


def run_decorator_exercises():
    """Runs tests and demonstrations of the advanced decorator concepts."""
    print("=" * 65)
    print(" 🧪 EXERCISE 1: Generic Logging Decorator (*args, **kwargs)")
    print("=" * 65)
    multiply_numbers(3, 4, c=5)
    multiply_numbers(10, 2)

    print("\n" + "=" * 65)
    print(" 🧪 EXERCISE 2: Authentication Guard Decorator")
    print("=" * 65)
    guest = User("Alice", is_logged_in=False)
    admin = User("Bob", is_logged_in=True)

    print("Attempting publish as unauthenticated user Alice:")
    create_blog_post(guest, "My Secret Python Tips")

    print("\nAttempting publish as authenticated user Bob:")
    create_blog_post(admin, "Flask Mastery in 100 Days")
