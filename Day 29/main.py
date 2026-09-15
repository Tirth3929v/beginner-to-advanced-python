import sys
from art import logo
from password_generator import generate_secure_password
from password_manager import start_password_manager

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution menu for Day 29 - MyPass Password Manager Studio."""
    print(logo)
    print("Welcome to Day 29 - MyPass Desktop Password Manager Studio! 🔐🛡️\n")

    try:
        while True:
            print("Choose an option:")
            print(" 1. 🖥️ Launch MyPass Desktop Password Manager (GUI)")
            print(" 2. ⚡ Quick Terminal Password Generator (CLI)")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                print("\n🚀 Launching MyPass Desktop Window...")
                start_password_manager()
                print("✅ MyPass closed.\n")
            elif choice == "2":
                pwd = generate_secure_password()
                print(f"\n🔑 Generated Secure Password: {pwd}\n")
            elif choice == "3":
                print("\nExiting MyPass Studio... Stay secure! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1, 2, or 3.\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting MyPass Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")
