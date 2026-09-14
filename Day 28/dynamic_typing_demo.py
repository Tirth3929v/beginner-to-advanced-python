import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_dynamic_typing_demos():
    """Demonstrates Python's dynamic typing vs statically typed languages."""
    print("\n⚡ Understanding Python Dynamic Typing")
    print("═" * 60)

    # 1. Variable type morphing during execution
    print("1️⃣ Variable Type Reassignment at Runtime:")
    a = 3
    print(f"   a = 3                  -> Value: {a:<10} | Type: {type(a)}")
    a = "Hello World"
    print(f"   a = 'Hello World'      -> Value: {a:<10} | Type: {type(a)}")
    a = [10, 20, 30]
    print(f"   a = [10, 20, 30]       -> Value: {str(a):<10} | Type: {type(a)}")
    a = {"status": "Active"}
    print(f"   a = {{'status': ...}}   -> Value: {str(a):<10} | Type: {type(a)}\n")

    # 2. Dynamic Typing in Pomodoro Timer
    print("2️⃣ Practical Application in the Pomodoro Timer:")
    print("   When formatting countdown seconds:")
    count_sec = 5  # Integer
    print(f"   count_sec = 5          -> Type: {type(count_sec)} (Calculated via count % 60)")
    if count_sec < 10:
        count_sec = f"0{count_sec}"  # Reassigned dynamically to String for zero-padded UI display
    print(f"   count_sec = f'0{{count_sec}}' -> Value: '{count_sec}' | Type: {type(count_sec)}")
    print("   This dynamic type shift makes UI string formatting effortless in Python!")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    try:
        run_dynamic_typing_demos()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")
