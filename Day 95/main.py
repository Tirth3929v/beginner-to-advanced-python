"""
Day 95: Custom 2D Racing Game
Phase 5: Portfolio

Key Concepts:
Turtle/Pygame 2D Engine, Obstacle Avoidance Vectors, Acceleration & Scores
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

from art import LOGO, RACER_SCENE
from racing_engine import RacingEngine, run_turtle_racer, TrafficCar


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print(RACER_SCENE)
    print("=" * 72)
    print(" 🚀 DAY 95: CUSTOM 2D RACING GAME")
    print(" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print(" Key Concepts: 2D Kinematics, Collision Vectors, Nitro Boost, Distance HUD")
    print("=" * 72 + "\n")


def run_automated_tests():
    """Validates the racing physics engine, velocity vectors, nitro, and collision checks."""
    print("\n🔍 Running Day 95 Automated 2D Racing Engine Test Suite...")
    print("-" * 70)

    engine = RacingEngine(track_width=36, track_height=22)

    # 1. Acceleration test
    initial_speed = engine.speed
    engine.accelerate(True)
    assert engine.speed > initial_speed, "Car failed to accelerate when throttle applied"
    print(" [PASS] 1. Vehicle throttle acceleration kinematics verified.")

    # 2. Braking test
    engine.speed = 100.0
    engine.brake()
    assert engine.speed < 100.0, "Brakes failed to decelerate vehicle"
    assert engine.speed >= engine.min_speed, "Speed dropped below minimum allowable threshold"
    print(" [PASS] 2. Brake deceleration and minimum speed clamping verified.")

    # 3. Steering and asphalt road boundaries
    engine.player_x = 5.0
    engine.steer("left") # Tries to steer off-road
    assert engine.player_x >= 4.0, "Vehicle breached left road shoulder boundary"
    engine.player_x = 30.0
    engine.steer("right")
    assert engine.player_x <= 31.0, "Vehicle breached right road shoulder boundary"
    print(" [PASS] 3. Lane steering constraints and road barrier containment verified.")

    # 4. Nitro boost activation & depletion
    initial_nitro = engine.nitro_gauge
    engine.speed = 100.0
    engine.trigger_nitro(True)
    assert engine.is_nitro_active is True
    assert engine.nitro_gauge < initial_nitro, "Nitro gauge failed to deplete upon usage"
    engine.trigger_nitro(False)
    assert engine.is_nitro_active is False
    print(" [PASS] 4. Nitrous Oxide (N2O) boost activation & fuel depletion verified.")

    # 5. Collision detection (AABB bounding box)
    test_traffic = TrafficCar(x=engine.player_x, y=engine.player_y, speed=40.0)
    engine.traffic = [test_traffic]
    engine.update_traffic_and_collisions()
    assert engine.crashed is True, "Collision engine failed to register vehicle crash"
    print(" [PASS] 5. AABB vehicular impact collision detection verified.")

    # 6. Distance integration
    engine.crashed = False
    engine.speed = 72.0 # 72 km/h = 20 m/s -> in 0.1s = 2.0 meters
    old_dist = engine.distance
    engine.step()
    assert round(engine.distance - old_dist, 1) == 2.0, "Distance integration math inaccurate"
    print(" [PASS] 6. Velocity-over-time distance accrual calculus verified.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! 2D Turbo Racing Engine fully operational.\n")


def run_ai_driver_simulation(ticks: int = 35):
    """Runs autonomous AI pilot navigating highway traffic."""
    print("\n  🏎️ Starting Autonomous AI Driver Simulation...")
    engine = RacingEngine(track_width=36, track_height=20)
    engine.speed = 90.0

    for t in range(ticks):
        if engine.crashed:
            print("\n  💥 Crash in simulation! Resetting...")
            break

        # AI pilot: detect traffic in current lane and switch to clearest lane
        danger_in_lane = any(
            abs(c.x - engine.player_x) < 4.0 and c.y < engine.track_height - 3.0
            for c in engine.traffic
        )

        steer_cmd = None
        if danger_in_lane:
            # Pick a lane center furthest from obstacles
            best_lane = min(
                engine.lane_centers,
                key=lambda l: sum(1.0 / (abs(c.y - engine.player_y) + 0.1) for c in engine.traffic if abs(c.x - l) < 4.0)
            )
            steer_cmd = "left" if best_lane < engine.player_x else "right"

        engine.step(steer_dir=steer_cmd, accelerate=True, nitro=(t % 8 == 0))

        if t % 3 == 0:
            print(f"\n--- [Tick {t + 1}/{ticks}] ---")
            print(engine.render_ascii_frame())
            time.sleep(0.08)

    print(f"\n  [✓] Simulation completed! Distance Traveled: {int(engine.distance)}m | Score: {engine.score}\n")


def interactive_cli():
    """Interactive CLI menu."""
    banner()

    while True:
        print("\n" + "=" * 55)
        print("  CUSTOM 2D RACING GAME MENU")
        print("=" * 55)
        print("  [1] Watch Autonomous AI Driver Simulation (Terminal ASCII)")
        print("  [2] Launch Desktop Turtle GUI Racer (Playable)")
        print("  [3] Run Automated Test Suite")
        print("  [4] Exit")
        print("=" * 55)

        choice = input("Enter option (1-4): ").strip()

        if choice == "1":
            run_ai_driver_simulation()
        elif choice == "2":
            try:
                run_turtle_racer()
            except Exception as e:
                print(f"  [!] Turtle display note: {e}")
                print("  Running terminal simulation instead...")
                run_ai_driver_simulation()
        elif choice == "3":
            run_automated_tests()
        elif choice == "4":
            print("\n👋 Exiting 2D Racing Game. Drive safe!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-4.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 95 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
