"""
Day 94: Space Invaders 2D Arcade Game
Phase 5: Portfolio

Key Concepts:
Python Turtle Engine, Alien Fleet Movement Vectors, Laser Collisions, Audio
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

from art import LOGO, INVADER_SCENE
from space_engine import SpaceInvadersEngine, run_turtle_game, Alien, Laser


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print(INVADER_SCENE)
    print("=" * 72)
    print(" 🚀 DAY 94: SPACE INVADERS 2D ARCADE GAME")
    print(" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print(" Key Concepts: Arcade Physics, Fleet Vectors, Laser Collisions, Bunkers")
    print("=" * 72 + "\n")


def run_automated_tests():
    """Validates the Space Invaders engine kinematics, collisions, and state machines."""
    print("\n🔍 Running Day 94 Automated Space Invaders Arcade Test Suite...")
    print("-" * 70)

    engine = SpaceInvadersEngine(width=50, height=24)

    # 1. Fleet spawning test
    assert len(engine.aliens) == 24, f"Expected 24 aliens, found {len(engine.aliens)}"
    top_row = [a for a in engine.aliens if a.row == 0]
    assert len(top_row) == 8
    assert top_row[0].points == 30
    print(" [PASS] 1. Alien fleet grid initialization verified (3x8 grid, 24 invaders, points mapped).")

    # 2. Player laser firing
    fired = engine.fire_player_laser()
    assert fired is True
    assert len(engine.lasers) == 1
    assert engine.lasers[0].from_player is True
    assert engine.lasers[0].vy > 0
    print(" [PASS] 2. Laser cannon projectile kinematics verified (positive upward velocity).")

    # 3. Laser vs Alien collision
    target_alien = engine.aliens[0]
    engine.lasers = [Laser(x=target_alien.x, y=target_alien.y - 0.5, vy=1.0, from_player=True)]
    initial_score = engine.score
    engine.update_lasers()
    assert not target_alien.alive, "Alien was not destroyed on direct laser collision"
    assert engine.score == initial_score + target_alien.points, "Score did not increment"
    assert len(engine.lasers) == 0, "Laser did not dissipate upon impact"
    print(" [PASS] 3. Laser vs Alien AABB collision detection & score accrual verified.")

    # 4. Alien bomb vs Bunker degradation
    bunker = engine.bunkers[0]
    initial_health = bunker.health
    engine.lasers = [Laser(x=bunker.x, y=bunker.y + 0.5, vy=-0.8, from_player=False)]
    engine.update_lasers()
    assert bunker.health == initial_health - 1, "Bunker failed to absorb damage"
    print(" [PASS] 4. Defensive bunker damage absorption verified.")

    # 5. Alien bomb vs Player damage
    engine.lasers = [Laser(x=engine.player_x, y=engine.player_y + 0.5, vy=-0.8, from_player=False)]
    initial_lives = engine.player_lives
    engine.update_lasers()
    assert engine.player_lives == initial_lives - 1, "Player failed to lose life on alien bomb hit"
    print(" [PASS] 5. Player damage kinematics and life decrement verified.")

    # 6. Wave advancement
    for a in engine.aliens:
        a.alive = False
    engine.update_fleet()
    assert engine.wave == 2, "Wave failed to advance when all aliens were destroyed"
    assert len([a for a in engine.aliens if a.alive]) == 24, "Fleet failed to respawn in new wave"
    print(" [PASS] 6. Wave progression & fleet replenishment state machine verified.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! Space Invaders 2D Arcade Engine fully operational.\n")


def run_ai_autoplay(frames: int = 40):
    """Runs autonomous AI autoplay demonstrating tracking and shooting."""
    engine = SpaceInvadersEngine(width=50, height=20)
    print("\n  👾 Running Autonomous Space Invaders Simulation...")

    for f in range(frames):
        # AI strategy: find closest alien and align player_x
        alive = [a for a in engine.aliens if a.alive]
        if not alive or engine.game_over:
            break

        closest = min(alive, key=lambda a: a.y)
        action = None
        if abs(engine.player_x - closest.x) > 1.5:
            action = "left" if engine.player_x > closest.x else "right"
        else:
            action = "fire"

        engine.step(action)
        if f % 4 == 0:
            print(f"\n--- [Frame {f + 1}/{frames}] ---")
            print(engine.render_ascii_frame())
            time.sleep(0.1)

    print(f"\n  [✓] Simulation completed! Final Score: {engine.score} | Wave: {engine.wave}\n")


def interactive_cli():
    """Interactive CLI menu."""
    banner()

    while True:
        print("\n" + "=" * 55)
        print("  SPACE INVADERS ARCADE MENU")
        print("=" * 55)
        print("  [1] Watch Autonomous AI Autoplay (Terminal ASCII)")
        print("  [2] Launch Desktop Turtle GUI Game (Playable)")
        print("  [3] Run Automated Test Suite")
        print("  [4] Exit")
        print("=" * 55)

        choice = input("Enter option (1-4): ").strip()

        if choice == "1":
            run_ai_autoplay()
        elif choice == "2":
            try:
                run_turtle_game()
            except Exception as e:
                print(f"  [!] Turtle display note: {e}")
                print("  Running terminal simulation instead...")
                run_ai_autoplay()
        elif choice == "3":
            run_automated_tests()
        elif choice == "4":
            print("\n👋 Exiting Space Invaders. Happy Gaming!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-4.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 94 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
