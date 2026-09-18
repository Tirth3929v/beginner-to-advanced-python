"""
Day 85: Typing Speed Test Desktop & CLI Application
Interactive Typing Speed & Accuracy Benchmark CLI
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from typing_engine import TypingSpeedTest, SAMPLE_PASSAGES


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 85: REAL-TIME WORDS-PER-MINUTE (WPM) & ACCURACY BENCHMARK")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Typing Engine Mechanics:")
    print("  • Standardized Paris Metric: 5 Keystrokes = 1 Normalized Word")
    print("  • Gross WPM vs Net WPM (Factoring in error penalties)")
    print("  • Precise Character Alignment & Accuracy Percentage Scoring")
    print("  • Performance Classification from Beginner to Pro Master (90+ WPM)")
    print("=" * 76 + "\n")


def run_test(passage: str = None):
    tester = TypingSpeedTest(passage)
    print("\n📝 TYPING SPEED CHALLENGE")
    print("=" * 70)
    print("Type the following passage exactly as shown, then press ENTER:\n")
    print("\033[93m" + tester.target_text + "\033[0m\n")
    print("-" * 70)
    input("Press ENTER when you are ready to start typing...")

    print("\n⏱️ TIMER STARTED! Start typing below:")
    tester.start()
    user_input = input("\n> ")
    results = tester.finish(user_input)

    print("\n" + "=" * 70)
    print(" 🏆 YOUR TYPING PERFORMANCE REPORT")
    print("=" * 70)
    print(f"  • Net Speed:          \033[92m{results['net_wpm']} WPM\033[0m")
    print(f"  • Gross Speed:        {results['gross_wpm']} WPM")
    print(f"  • Accuracy:           \033[94m{results['accuracy_pct']}%\033[0m")
    print(f"  • Elapsed Time:       {results['elapsed_seconds']} seconds")
    print(f"  • Characters Typed:   {results['total_typed_chars']} ({results['correct_chars']} correct, {results['errors']} errors)")
    print(f"  • Skill Category:     \033[95m{results['tier']}\033[0m")
    print("=" * 70 + "\n")


def sprint_test():
    short_quote = "Python empowers developers to build clean software rapidly."
    run_test(short_quote)


def display_tiers():
    print("\n📊 TYPING SPEED BENCHMARK CLASSIFICATIONS")
    print("=" * 60)
    tiers = [
        ("0 - 30 WPM", "Beginner / Hunt & Peck", "Learning finger positioning"),
        ("30 - 50 WPM", "Average Typist", "Typical office / everyday speed"),
        ("50 - 70 WPM", "Fluent / Productive", "Comfortable touch typing"),
        ("70 - 90 WPM", "Fast Typist", "High-efficiency coding / transcription"),
        ("90+ WPM", "Pro Master / Elite", "Competitive speed typist")
    ]
    for speed, rank, desc in tiers:
        print(f"  • {speed:<14} \033[92m{rank:<22}\033[0m ({desc})")
    print("=" * 60 + "\n")


def run_automated_tests():
    """Verifies WPM math, accuracy calculation, and error penalty scoring."""
    print("\n🔍 Running Day 85 Automated Typing Engine Verification Suite...")
    print("-" * 70)

    target = "The quick brown fox jumps over the lazy dog."
    tester = TypingSpeedTest(target)

    # 1. Perfect typing test (100% accuracy)
    perfect_res = tester.calculate_metrics(target, elapsed_seconds=60.0) # took exactly 1 minute
    expected_wpm = len(target) / 5.0
    assert perfect_res["accuracy_pct"] == 100.0
    assert perfect_res["gross_wpm"] == expected_wpm
    assert perfect_res["net_wpm"] == expected_wpm
    assert perfect_res["errors"] == 0
    print(f" [PASS] 1. Perfect typing score verified: {perfect_res['net_wpm']} WPM at 100% accuracy.")

    # 2. Typing with errors test
    mistyped = "The quick brown cat jumps over the lazy dog." # 'fox' -> 'cat' (3 errors)
    err_res = tester.calculate_metrics(mistyped, elapsed_seconds=30.0)
    assert err_res["accuracy_pct"] < 100.0
    assert err_res["net_wpm"] < err_res["gross_wpm"]
    print(f" [PASS] 2. Error penalty scoring verified: Gross ({err_res['gross_wpm']}) > Net ({err_res['net_wpm']}).")

    # 3. High-speed pro classification
    fast_res = tester.calculate_metrics(target, elapsed_seconds=5.0) # 5 seconds
    assert "90+ WPM" in fast_res["tier"] or "Pro" in fast_res["tier"]
    print(" [PASS] 3. Elite performance tier classification verified.")

    print("-" * 70)
    print("✨ ALL 3 TESTS PASSED! Typing Speed Test Engine fully operational.\n")


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) ⏱️ Take Standard Typing Speed Test (Paragraph)")
        print("  2) ⚡ Quick 1-Sentence Speed Sprint")
        print("  3) 📊 View Typing Speed Benchmark Classifications")
        print("  4) ✅ Run Automated Verification Suite (3 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            run_test()
        elif choice == "2":
            sprint_test()
        elif choice == "3":
            display_tiers()
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Keep typing fast and clean! ⌨️\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 85 gracefully... Goodbye!\n")
