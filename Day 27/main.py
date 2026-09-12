import sys
from args_kwargs_demo import run_args_kwargs_demos
from art import logo
from miles_to_km import start_miles_to_km_app
from unit_converter_gui import start_multi_converter

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution menu for Day 27 - Tkinter GUI & *args/**kwargs Studio."""
    print(logo)
    print("Welcome to Day 27 - Tkinter GUI & Python Function Arguments Studio! 🖥️⚙️\n")

    try:
        while True:
            print("Choose an application or demo to launch:")
            print(" 1. 🚗 Miles to Kilometers Converter (Classic Tkinter)")
            print(" 2. 🔄 OmniConverter Pro (Multi-Unit Desktop GUI)")
            print(" 3. ⚙️  *args and **kwargs Deep Dive Playground")
            print(" 4. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-4): ").strip()
            if choice == "1":
                print("\n🚀 Launching Miles to Km Desktop App...")
                start_miles_to_km_app()
                print("✅ Window closed.\n")
            elif choice == "2":
                print("\n🚀 Launching OmniConverter Pro Desktop App...")
                start_multi_converter()
                print("✅ Window closed.\n")
            elif choice == "3":
                run_args_kwargs_demos()
            elif choice == "4":
                print("\nExiting Tkinter Studio... Goodbye! 👋\n")
                break
            else:
                print("⚠️ Invalid selection! Please enter 1, 2, 3, or 4.\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Tkinter Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")
