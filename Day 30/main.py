"""
Day 30 - Errors, Exceptions & JSON Data Studio
Main launcher connecting all Day 30 modules:
- Exception Handling Lifecycle & Practice Lab
- Resilient NATO Phonetic Alphabet V2
- Resilient JSON Vault Engine (GUI & CLI)
"""

import sys
from art import logo
from exception_lab import explain_try_except_flow, run_all_exercises
from json_vault import launch_gui_vault, run_terminal_vault_explorer
from nato_phonetic_v2 import run_nato_encoder_resilient

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution studio loop for Day 30."""
    print(logo)
    print("Welcome to Day 30 - Errors, Exceptions & Resilient JSON Studio! 🛡️💻\n")

    try:
        while True:
            print("Select an option to run:")
            print(" 1. 🖥️ Launch Resilient JSON Vault (Desktop GUI)")
            print(" 2. 📂 Terminal JSON Vault Explorer (CRUD & Error Testing)")
            print(" 3. 📡 NATO Phonetic Alphabet V2 (KeyError Recovery)")
            print(" 4. 🧪 Exception Handling Laboratory (All Curriculum Exercises)")
            print(" 5. 📚 Try-Except-Else-Finally Flow Demonstration")
            print(" 6. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-6): ").strip()
            if choice == "1":
                print("\n🚀 Launching Resilient JSON Vault Desktop GUI...")
                launch_gui_vault()
                print("✅ GUI closed.\n")
            elif choice == "2":
                run_terminal_vault_explorer()
            elif choice == "3":
                run_nato_encoder_resilient()
            elif choice == "4":
                run_all_exercises()
            elif choice == "5":
                explain_try_except_flow()
            elif choice == "6":
                print("\nExiting Day 30 Studio... Happy error-free coding! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please enter a number between 1 and 6.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 30 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")
