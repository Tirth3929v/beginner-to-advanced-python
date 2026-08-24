import sys
import io
import time
from art import logo

# Fix UTF-8 encoding output on Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ==========================================
# 🐞 BUG SNIPPET REPOSITORY & BUGGY/FIXED LOGIC
# ==========================================

# Case 1: Off-by-One / Boundary Error
def buggy_range(n):
    result = []
    # Bug: range(1, n) stops at n-1 instead of n
    for i in range(1, n):
        result.append(i)
    return result

def fixed_range(n):
    result = []
    for i in range(1, n + 1):
        result.append(i)
    return result

# Case 2: Operator Precedence / Evaluation Order in FizzBuzz
def buggy_fizzbuzz(n):
    # Bug: n % 3 == 0 evaluated first, blocking numbers divisible by 15 from returning 'FizzBuzz'
    if n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    elif n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    else:
        return str(n)

def fixed_fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)

# Case 3: Mutable Default Argument State Leak
def buggy_append(item, target_list=[]):
    # Bug: target_list default is evaluated once at definition time, persisting state across calls
    target_list.append(item)
    return target_list

def fixed_append(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list

# Case 4: Century Leap-Year Logic
def buggy_leap_year(year):
    # Bug: year % 4 == 0 alone flags century years (e.g. 1900, 2100) incorrectly as leap years
    if year % 4 == 0:
        return True
    else:
        return False

def fixed_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False

# Case 5: List Mutation During Iteration / Index Skipping
def buggy_remove_evens(numbers):
    # Bug: Modifying numbers while iterating skips elements due to re-indexing
    for num in numbers:
        if num % 2 == 0:
            numbers.remove(num)
    return numbers

def fixed_remove_evens(numbers):
    return [num for num in numbers if num % 2 != 0]


CASES = [
    {
        "id": "CASE-101",
        "title": "The Boundary Slip",
        "category": "Off-by-One / Range Boundary Error",
        "description": "Function intended to return a list of integers from 1 up to and including 'n'.",
        "broken_code": """def generate_sequence(n):
    result = []
    for i in range(1, n):  # <-- Is 'n' included?
        result.append(i)
    return result""",
        "options": [
            "SyntaxError: Invalid keyword in range function",
            "Off-by-One Error: range(1, n) omits upper bound 'n'",
            "TypeError: Cannot iterate over integer n",
            "Recursion Limit Exceeded"
        ],
        "correct_option": 1,
        "explanation": "In Python, range(start, stop) excludes the 'stop' value. To include 'n', range(1, n + 1) must be used.",
        "buggy_func": lambda: buggy_range(5),
        "fixed_func": lambda: fixed_range(5),
        "tests": [
            ("generate_sequence(5)", [1, 2, 3, 4, 5], lambda: buggy_range(5), lambda: fixed_range(5)),
            ("generate_sequence(1)", [1], lambda: buggy_range(1), lambda: fixed_range(1)),
        ]
    },
    {
        "id": "CASE-102",
        "title": "The Precedence Trap (FizzBuzz)",
        "category": "Logical Precedence / Unreachable Code",
        "description": "Evaluates divisible numbers: 3 -> 'Fizz', 5 -> 'Buzz', 15 -> 'FizzBuzz'.",
        "broken_code": """def fizz_buzz(n):
    if n % 3 == 0:           # <-- 15 triggers this first!
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    elif n % 3 == 0 and n % 5 == 0:  # <-- Unreachable code!
        return "FizzBuzz"
    else:
        return str(n)""",
        "options": [
            "Modulo % operation is illegal for integers",
            "Logical / Order of Evaluation Flaw: 15 is matched by n % 3 == 0 first",
            "IndentationError on elif statement",
            "Type Mismatch: Returning string instead of int"
        ],
        "correct_option": 1,
        "explanation": "More specific conditions (like n % 15 == 0) must be checked BEFORE broader conditions (n % 3 == 0), otherwise the broader condition shadow-matches first.",
        "tests": [
            ("fizz_buzz(15)", "FizzBuzz", lambda: buggy_fizzbuzz(15), lambda: fixed_fizzbuzz(15)),
            ("fizz_buzz(9)", "Fizz", lambda: buggy_fizzbuzz(9), lambda: fixed_fizzbuzz(9)),
        ]
    },
    {
        "id": "CASE-103",
        "title": "The Ghost List (State Leak)",
        "category": "Mutable Default Argument Bug",
        "description": "Function appends an item to a default list parameter across multiple function calls.",
        "broken_code": """def append_to_list(item, target_list=[]): # <-- Mutable default arg!
    target_list.append(item)
    return target_list

# Call 1: append_to_list('A') -> ['A']
# Call 2: append_to_list('B') -> Expected ['B'], Actual: ['A', 'B']""",
        "options": [
            "SyntaxError: Default argument cannot be a list",
            "State Mutation Bug: Default argument list [] is evaluated once at function definition and shared across calls",
            "IndexError: Cannot append to an empty list",
            "NameError: target_list is not defined in global scope"
        ],
        "correct_option": 1,
        "explanation": "Default argument expressions in Python are evaluated once when the function is defined, NOT on each execution. Use target_list=None and initialize inside the function body.",
        "tests": [
            ("append_to_list('X')", ['X'], lambda: buggy_append('X'), lambda: fixed_append('X')),
            ("append_to_list('Y') (Second invocation)", ['Y'], lambda: buggy_append('Y'), lambda: fixed_append('Y')),
        ]
    },
    {
        "id": "CASE-104",
        "title": "The Century Glitch",
        "category": "Incomplete Business Logic",
        "description": "Determines whether a given year is a Leap Year according to the Gregorian calendar.",
        "broken_code": """def is_leap_year(year):
    if year % 4 == 0:  # <-- Fails on century years like 1900 or 2100!
        return True
    else:
        return False""",
        "options": [
            "ZeroDivisionError: year could be 0",
            "Logical Flaw: Century years divisible by 100 are NOT leap years unless also divisible by 400",
            "TypeError: % operator requires float operands",
            "Infinite Loop Error"
        ],
        "correct_option": 1,
        "explanation": "Leap year rules require: Divisible by 4 AND NOT divisible by 100 UNLESS also divisible by 400. Simply checking % 4 is insufficient for century years like 1900.",
        "tests": [
            ("is_leap_year(1900)", False, lambda: buggy_leap_year(1900), lambda: fixed_leap_year(1900)),
            ("is_leap_year(2000)", True, lambda: buggy_leap_year(2000), lambda: fixed_leap_year(2000)),
        ]
    },
    {
        "id": "CASE-105",
        "title": "The Skipping Loop",
        "category": "In-Place Collection Mutation",
        "description": "Function filters out even numbers from a list in-place.",
        "broken_code": """def remove_evens(numbers):
    for num in numbers:
        if num % 2 == 0:
            numbers.remove(num)  # <-- Modifying list while iterating!
    return numbers""",
        "options": [
            "KeyError: Element num not found in numbers",
            "Iteration Bug: Removing elements from a list while iterating shifts indices, causing elements to be skipped",
            "AttributeError: List object has no remove method",
            "Memory Leak Error"
        ],
        "correct_option": 1,
        "explanation": "Never mutate a list while iterating over it directly. Internal index pointers advance past elements when an item is removed. Use list comprehension or iterate over a shallow copy.",
        "tests": [
            ("remove_evens([2, 4, 6, 7])", [7], lambda: buggy_remove_evens([2, 4, 6, 7]), lambda: fixed_remove_evens([2, 4, 6, 7])),
            ("remove_evens([1, 3, 5])", [1, 3, 5], lambda: buggy_remove_evens([1, 3, 5]), lambda: fixed_remove_evens([1, 3, 5])),
        ]
    }
]


def print_banner():
    print(logo)
    print("======================================================================")
    print("   🔍 WELCOME, DETECTIVE! INITIALIZING CODE AUDITING ENVIRONMENT...")
    print("   🎯 Mission: Audit 5 real-world Python bug cases & verify fixes.")
    print("======================================================================\n")

def run_assertion_suite(case):
    print("\n  ⚙️ RUNNING LIVE ASSERTION SUITE...")
    print("  ------------------------------------------------------------------")
    all_passed = True
    
    for idx, (test_name, expected, buggy_fn, fixed_fn) in enumerate(case["tests"], 1):
        # 1. Run buggy function
        actual_buggy = buggy_fn()
        buggy_passed = actual_buggy == expected
        
        print(f"\n  🧪 Test {idx}: {test_name}")
        print(f"     Expected Result: {expected}")
        print(f"     Buggy Exec:     {actual_buggy} -> ", end="")
        if buggy_passed:
            print("🟢 [UNEXPECTED PASS]")
        else:
            print("🔴 [FAIL - BUG CONFIRMED!]")
            all_passed = False

        # 2. Run fixed function
        actual_fixed = fixed_fn()
        fixed_passed = actual_fixed == expected
        print(f"     Fixed Exec:     {actual_fixed} -> ", end="")
        if fixed_passed:
            print("🟢 [PASS - ASSERTION CLEARED]")
        else:
            print("🔴 [FAIL]")

    print("  ------------------------------------------------------------------")
    return not buggy_passed and fixed_passed

def play_case(case_num, case, score):
    print(f"\n======================================================================")
    print(f"  📂 [{case['id']}] CASE #{case_num}: {case['title'].upper()}")
    print(f"  🏷️ Category: {case['category']}")
    print(f"======================================================================")
    print(f"\n📋 Scenario Description:")
    print(f"   {case['description']}\n")
    print("💻 Code Snippet under Audit:")
    print("----------------------------------------------------------------------")
    for line in case['broken_code'].split("\n"):
        print(f"   {line}")
    print("----------------------------------------------------------------------")

    print("\n🔍 Select the correct Diagnosis:")
    for idx, option in enumerate(case["options"], 1):
        print(f"   [{idx}] {option}")

    while True:
        try:
            choice = int(input("\n👉 Enter Diagnosis Choice (1-4): "))
            if 1 <= choice <= 4:
                selected_idx = choice - 1
                break
            else:
                print("  ⚠️ Invalid selection. Please enter a number between 1 and 4.")
        except ValueError:
            print("  ⚠️ Invalid input. Please enter a valid number.")

    is_correct = (selected_idx == case["correct_option"])
    
    if is_correct:
        print("\n  🏆 [CORRECT DIAGNOSIS!] Excellent investigation, Detective!")
        score += 20
    else:
        correct_text = case["options"][case["correct_option"]]
        print(f"\n  ❌ [INCORRECT DIAGNOSIS] Target bug was: {correct_text}")

    print(f"\n💡 Forensic Breakdown:")
    print(f"   {case['explanation']}")

    # Run assertion suite to verify fix mechanics
    run_assertion_suite(case)
    
    time.sleep(1)
    return score

def main():
    while True:
        print_banner()
        score = 0
        total_cases = len(CASES)

        for idx, case in enumerate(CASES, 1):
            score = play_case(idx, case, score)
            if idx < total_cases:
                input("\n  ⏩ Press Enter to proceed to the next Case File...")

        # Final Score Summary
        print("\n======================================================================")
        print("  📊 AUDIT SUMMARY REPORT - PYDETECTIVE CASE CLOSURE")
        print("======================================================================")
        print(f"  🎯 Final Detective Score: {score} / 100 Points")
        
        if score == 100:
            badge = "🥇 MASTER CODE AUDITOR (Rank S)"
            msg = "Flawless performance! You identified all logical traps and state mutations."
        elif score >= 60:
            badge = "🥈 SENIOR DETECTIVE (Rank A)"
            msg = "Great debugging skills! Most edge cases were identified."
        else:
            badge = "🥉 JUNIOR AUDITOR (Rank B)"
            msg = "Good effort! Practice inspecting state leaks and evaluation order."

        print(f"  🏅 Rank Achieved: {badge}")
        print(f"  📝 Feedback: {msg}")
        print("======================================================================\n")

        play_again = input("🔄 Audit another suite of cases? (y/n): ").strip().lower()
        if play_again != 'y':
            print("\n  👋 [CASE CLOSED] Thank you for keeping the codebase bug-free! Goodbye! ✨\n")
            break

if __name__ == "__main__":
    main()
