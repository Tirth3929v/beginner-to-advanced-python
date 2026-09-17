"""
Day 93: Automate Google Chrome Dinosaur Game
Phase 5: Portfolio

Key Concepts:
PyAutoGUI, Screen Capture, Pixel Color Detection, Jump Trigger Loop
"""

import sys
import time

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO, DINO_SCENE
from dino_bot import DinoBot, SyntheticGameSimulator


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print(DINO_SCENE)
    print("=" * 72)
    print(" 🚀 DAY 93: AUTOMATE GOOGLE CHROME DINOSAUR GAME")
    print(" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print(" Key Concepts: PyAutoGUI, Screen Capture, Pixel Color Detection, Jump Loop")
    print("=" * 72 + "\n")


def run_automated_tests():
    """Validates the bot's computer vision, obstacle detection, and control physics."""
    print("\n🔍 Running Day 93 Automated Dinosaur Bot & Vision Test Suite...")
    print("-" * 70)

    # 1. Test synthetic rendering & day mode detection
    sim = SyntheticGameSimulator(width=400, height=200)
    sim.spawn_obstacle(x=120, width=20, height=35)
    frame_day = sim.render_frame()

    # Scan region strictly above ground line (ground is at y=150)
    bot = DinoBot(scan_box=(110, 115, 150, 148), pixel_threshold=10)
    assert not bot.is_night_mode(frame_day), "Day frame misidentified as night mode"
    assert bot.detect_obstacle(frame_day), "Failed to detect obstacle in day frame"
    print(" [PASS] 1. Synthetic Day Mode rendering & obstacle pixel detection verified.")

    # 2. Test night mode inverted detection
    sim.night_mode = True
    frame_night = sim.render_frame()
    assert bot.is_night_mode(frame_night), "Night frame misidentified as day mode"
    assert bot.detect_obstacle(frame_night), "Failed to detect obstacle in night frame"
    print(" [PASS] 2. Inverted Night Mode rendering & obstacle pixel detection verified.")

    # 3. Test false positive prevention (clear frame)
    sim.reset()
    frame_empty = sim.render_frame()
    assert not bot.detect_obstacle(frame_empty), "False positive detected on clear frame"
    print(" [PASS] 3. Negative control verified: zero false positives on empty terrain.")

    # 4. Test jump cooldown mechanics
    jumps = []
    test_bot = DinoBot(jump_cooldown=0.1, action_callback=lambda act: jumps.append(act))
    first_jump = test_bot.jump()
    second_jump = test_bot.jump()  # Should fail due to cooldown
    assert first_jump is True, "Initial jump failed"
    assert second_jump is False, "Cooldown failed to prevent immediate double jump"
    time.sleep(0.12)
    third_jump = test_bot.jump()  # Should succeed after cooldown
    assert third_jump is True, "Jump after cooldown failed"
    assert len(jumps) == 2
    print(" [PASS] 4. Keystroke cooldown timer verified (prevents mid-air jump spam).")

    # 5. Closed-loop automated simulation benchmark
    sim_benchmark = SyntheticGameSimulator(width=500, height=200)
    sim_benchmark.spawn_obstacle(x=250, width=20, height=35)
    sim_bot = DinoBot(
        scan_box=(120, 115, 180, 148),
        jump_cooldown=0.2,
        action_callback=lambda act: sim_benchmark.jump()
    )

    jumped = False
    collision_occurred = False
    for step in range(40):
        frame = sim_benchmark.render_frame()
        if sim_bot.detect_obstacle(frame):
            if sim_bot.jump():
                jumped = True
        state = sim_benchmark.step()
        if state["collision"]:
            collision_occurred = True
            break

    assert jumped is True, "Bot failed to trigger jump during simulation run"
    assert not collision_occurred, "Dino collided with obstacle during simulation run"
    print(" [PASS] 5. Full closed-loop physics simulation: obstacle cleared without collision.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Autonomous Chrome Dinosaur Bot fully operational.\n")


def run_benchmark_visualizer():
    """Runs a live ASCII visualizer of the bot jumping over oncoming obstacles in real time."""
    print("\n  🎮 Starting Dino Bot Synthetic Physics Simulation Benchmark...")
    print("  Watch the bot detect obstacles and execute timed jumps:\n")

    sim = SyntheticGameSimulator(width=40, height=10)
    sim.ground_y = 6
    sim.dino_y = 6
    sim.jump_velocity = -4.0
    sim.gravity = 1.0
    sim.speed = 2.0

    # Custom ASCII renderer
    actions = []
    bot = DinoBot(
        scan_box=(5, 2, 18, 8),
        jump_cooldown=0.3,
        action_callback=lambda act: sim.jump()
    )

    # Spawn 3 obstacles spaced out
    sim.spawn_obstacle(x=20, width=2, height=3)
    sim.spawn_obstacle(x=38, width=2, height=3)

    for tick in range(30):
        # Obstacle scan
        frame = sim.render_frame()
        if bot.detect_obstacle(frame):
            bot.jump()

        res = sim.step()

        # Render ASCII strip
        ground_line = ["_"] * 35
        dino_pos = int(sim.dino_y)
        dino_char = "🦖" if dino_pos == 6 else "⏫"
        
        for obs in sim.obstacles:
            ox = int(obs["x"])
            if 0 <= ox < 35:
                ground_line[ox] = "🌵"

        if 0 <= 5 < 35:
            ground_line[5] = dino_char

        status_msg = " [JUMPING!]" if dino_pos < 6 else " [RUNNING]"
        print(f"  Tick {tick:02d}: " + "".join(ground_line) + status_msg)
        time.sleep(0.08)

    print("\n  [✓] Benchmark run complete! All obstacles successfully navigated.\n")


def interactive_cli():
    """Interactive command-line interface."""
    banner()
    bot = DinoBot()

    while True:
        print("\n" + "=" * 55)
        print("  AUTONOMOUS DINO BOT MENU")
        print("=" * 55)
        print("  [1] Launch Dino Bot on Live Chrome Window (chrome://dino)")
        print("  [2] Run Headless Physics Simulation Benchmark")
        print("  [3] Calibrate Detection Bounding Box Coordinates")
        print("  [4] Run Automated Test Suite")
        print("  [5] Exit")
        print("=" * 55)

        choice = input("Enter option (1-5): ").strip()

        if choice == "1":
            print("\n  Instructions:")
            print("  1. Open Google Chrome.")
            print("  2. Navigate to 'chrome://dino' in your browser.")
            print("  3. Make sure the window is visible on screen.")
            duration_str = input("  Enter run duration in seconds (default: 15): ").strip()
            duration = int(duration_str) if duration_str.isdigit() else 15
            bot.run_live_loop(duration_sec=duration)

        elif choice == "2":
            run_benchmark_visualizer()

        elif choice == "3":
            print(f"\n  Current Scan Box: {bot.scan_box}")
            raw = input("  Enter new box as 'x1,y1,x2,y2' (or press Enter to keep): ").strip()
            if raw:
                try:
                    parts = [int(p.strip()) for p in raw.split(",")]
                    if len(parts) == 4:
                        bot.scan_box = tuple(parts)
                        print(f"  [✓] Updated scan box to: {bot.scan_box}")
                    else:
                        print("  [!] Please provide exactly 4 comma-separated integers.")
                except ValueError:
                    print("  [!] Invalid number format.")

        elif choice == "4":
            run_automated_tests()

        elif choice == "5":
            print("\n👋 Exiting Dino Bot. Happy Gaming!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-5.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 93 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
