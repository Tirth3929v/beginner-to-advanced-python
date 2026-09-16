"""
Day 30 - Exception Handling Laboratory
Interactive demonstrations, standard curriculum exercises, and custom exception raising.
"""

import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def explain_try_except_flow():
    """Explains and demonstrates the complete try - except - else - finally lifecycle."""
    print("\n" + "=" * 65)
    print(" 📚 THE COMPLETE TRY - EXCEPT - ELSE - FINALLY LIFECYCLE")
    print("=" * 65)
    print(r"""
  ┌──────────────────────────────────────────────────────────┐
  │ try:                                                     │
  │     # Code that might cause an exception                 │
  │ except SpecificError as error:                           │
  │     # Executes ONLY if the specific exception occurred   │
  │ else:                                                    │
  │     # Executes ONLY if NO exceptions occurred in try     │
  │ finally:                                                 │
  │     # Executes ALWAYS, no matter what happens            │
  └──────────────────────────────────────────────────────────┘
    """)
    print("Demonstration running with user-provided numerator and denominator:")

    try:
        num_str = input("👉 Enter a numerator number (e.g. 100): ").strip()
        den_str = input("👉 Enter a denominator number (e.g. 5): ").strip()

        numerator = float(num_str)
        denominator = float(den_str)

        print("\n [1] Inside 'try' block: Performing division...")
        result = numerator / denominator

    except ValueError as val_err:
        print(f"\n [2] ❌ 'except ValueError' caught: Invalid numeric input! ({val_err})")
    except ZeroDivisionError as zero_err:
        print(f"\n [2] ❌ 'except ZeroDivisionError' caught: Cannot divide by zero! ({zero_err})")
    else:
        print(f"\n [3] ✨ 'else' block reached: Success! {numerator} / {denominator} = {result:.4f}")
    finally:
        print(" [4] 🔒 'finally' block: Cleanup actions always execute!\n")


def run_index_error_exercise():
    """Exercise 1: IndexError handling (Fruit Pie)."""
    print("\n" + "=" * 65)
    print(" 🥧 EXERCISE 1: IndexError Handling (Fruit Pie Maker)")
    print("=" * 65)
    print("Problem: Safely retrieve pie ingredients by index without crashing.\n")

    fruits = ["Apple", "Pear", "Orange", "Banana", "Cherry"]
    print(f"Available fruit inventory: {fruits}")

    def make_pie(index: int):
        try:
            fruit = fruits[index]
        except IndexError:
            print(f"⚠️ Index [{index}] is out of range! Defaulting to 'Fruit Pie'.")
            return "Fruit Pie"
        else:
            return f"{fruit} Pie"

    for idx in [0, 2, 4, 5, 10]:
        pie = make_pie(idx)
        print(f" -> Order at index {idx:2d}: {pie}")
    print("\n✅ All orders processed safely without crashing!\n")


def run_key_error_exercise():
    """Exercise 2: KeyError handling (Social Media Post Likes Counter)."""
    print("\n" + "=" * 65)
    print(" 📱 EXERCISE 2: KeyError Handling (Social Post Likes Aggregator)")
    print("=" * 65)
    print("Problem: Sum total likes from a list of post dictionaries, where some posts have NO 'Likes' key.\n")

    facebook_posts = [
        {"Likes": 21, "Comments": 2},
        {"Likes": 13, "Comments": 2, "Shares": 1},
        {"Likes": 33, "Comments": 8, "Shares": 3},
        {"Comments": 4, "Shares": 2},  # Missing 'Likes' key!
        {"Comments": 1, "Shares": 1},  # Missing 'Likes' key!
        {"Likes": 19, "Comments": 3}
    ]

    total_likes = 0
    skipped_posts = 0

    for i, post in enumerate(facebook_posts, 1):
        try:
            likes = post["Likes"]
            total_likes += likes
            print(f" Post #{i}: Found {likes} likes.")
        except KeyError:
            skipped_posts += 1
            print(f" Post #{i}: ⚠️ KeyError! Missing 'Likes' key, defaulted to 0 likes.")

    print(f"\n📊 Total Likes Aggregated: {total_likes}")
    print(f"🛡️ Gracefully handled {skipped_posts} posts missing the 'Likes' key.\n")


def run_raise_exception_demo():
    """Exercise 3: Raising custom exceptions using `raise` keyword (BMI Calculator)."""
    print("\n" + "=" * 65)
    print(" ⚖️ EXERCISE 3: Raising Custom Exceptions with `raise`")
    print("=" * 65)
    print("Problem: Prevent illogical data (e.g. human height > 3 meters) by raising a ValueError.\n")

    try:
        height_str = input("👉 Enter height in meters (e.g. 1.75): ").strip()
        weight_str = input("👉 Enter weight in kg (e.g. 70): ").strip()

        height = float(height_str)
        weight = float(weight_str)

        if height <= 0:
            raise ValueError("Height must be strictly greater than 0 meters.")
        if height > 3.0:
            raise ValueError("Human height cannot realistically exceed 3.0 meters! (World record: 2.72m)")
        if weight <= 0 or weight > 650:
            raise ValueError(f"Weight of {weight}kg is outside valid human biological bounds (0 - 650kg).")

        bmi = weight / (height ** 2)
        print(f"\n✅ Calculated BMI: {bmi:.2f}")

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        print(f"📋 Classification: {category}\n")

    except ValueError as e:
        print(f"\n❌ Validation Error Caught: {e}\n")


def run_all_exercises():
    """Runs all 3 curriculum exercises in sequence."""
    run_index_error_exercise()
    run_key_error_exercise()
    run_raise_exception_demo()


if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    explain_try_except_flow()
