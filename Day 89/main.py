"""
Day 89: Disappearing Text Writing App
Interactive Flow State Writer CLI & Desktop Launcher
"""

import sys
import os
import time

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from disappearing_app import WritingSession, launch_tkinter_gui


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 89: DISAPPEARING TEXT WRITING APP (FLOW STATE ENGINE)")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Flow Psychology & Application Mechanics:")
    print("  • The Most Dangerous Writing Paradigm: Overcoming writer's block by urgency")
    print("  • Inactivity Countdown: 5.0s typing threshold before buffer wipe")
    print("  • Session Goal: Sustained continuous stream-of-consciousness writing")
    print("  • Dual Modes: Interactive Terminal Sprint and Tkinter Desktop GUI")
    print("=" * 76 + "\n")


def console_sprint():
    print("\n✍️ CONSOLE WRITING SPRINT (30-Second Target, 5s Inactivity Limit)")
    print("=" * 70)
    print("Rules: Type continuous sentences. If you pause for more than 5 seconds,")
    print("everything you wrote will be erased into oblivion!\n")
    input("Press ENTER to ignite the flow timer...")

    session = WritingSession(timeout_seconds=5.0, goal_seconds=30.0)
    print("\n⏱️ FLOW SESSION ACTIVE! Type and press ENTER repeatedly to keep going:")

    while True:
        line = input("> ").strip()
        active, rem, msg = session.check_status()
        if not active:
            if session.is_vanished:
                print("\n💥 TOO SLOW! You paused and your words dissolved into the ether.\n")
            elif session.is_completed:
                print(f"\n🎉 VICTORY! {msg}")
                path = session.save_work()
                print(f"Saved draft to: {path}\n")
            break

        session.on_keystroke(session.buffer + " " + line)
        print(f"   [Keep typing! Time until erase: {session.timeout_seconds:.1f}s]")


def run_automated_tests():
    """Verifies keystroke recording, inactivity timeout buffer wipe, and goal victory."""
    print("\n🔍 Running Day 89 Automated Flow State Writing Engine Test Suite...")
    print("-" * 70)

    # 1. Keystroke buffer recording
    session = WritingSession(timeout_seconds=2.0, goal_seconds=10.0)
    session.on_keystroke("Hello world flow state")
    assert session.buffer == "Hello world flow state"
    assert session.is_vanished is False
    print(" [PASS] 1. Keystroke buffer recording and state initialization verified.")

    # 2. Active status check before timeout
    active, rem, msg = session.check_status(now=session.last_keystroke_time + 1.0)
    assert active is True
    assert rem > 0.5
    print(" [PASS] 2. Active timer countdown decrement verified.")

    # 3. Timeout expiration & Buffer wipe
    active, rem, msg = session.check_status(now=session.last_keystroke_time + 2.5)
    assert active is False
    assert session.is_vanished is True
    assert session.buffer == ""
    print(" [PASS] 3. Inactivity penalty: Text buffer erased to 0 characters upon timeout.")

    # 4. Goal victory verification
    goal_session = WritingSession(timeout_seconds=5.0, goal_seconds=10.0)
    goal_session.on_keystroke("A sustained creative paragraph that reaches the goal.")
    active, rem, msg = goal_session.check_status(now=goal_session.session_start_time + 10.5)
    assert active is False
    assert goal_session.is_completed is True
    saved = goal_session.save_work("test_draft.txt")
    assert saved is not None and os.path.exists(saved)
    try:
        os.remove(saved)
    except Exception:
        pass
    print(" [PASS] 4. Session goal achievement & file persistence verified.")

    print("-" * 70)
    print("✨ ALL 4 TESTS PASSED! Disappearing Text Writing Engine fully operational.\n")


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) ⏱️ Take Console Flow Writing Sprint (30-Second Challenge)")
        print("  2) 🖥️ Launch Desktop Graphical App (Tkinter with fading text)")
        print("  3) ✅ Run Automated Verification Suite (4 Unit Tests)")
        print("  4) 🚪 Exit")
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            console_sprint()
        elif choice == "2":
            launch_tkinter_gui(timeout=5, goal_seconds=60)
        elif choice == "3":
            run_automated_tests()
        elif choice in ("4", "exit", "quit", "q"):
            print("\n👋 Never stop writing! Keep the flow alive ✍️\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-4.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 89 gracefully... Goodbye!\n")
