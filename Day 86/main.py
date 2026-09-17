"""
Day 86: Breakout Arcade Game
2D Physics, Collision Detection, and Arcade Simulation CLI
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
from breakout_engine import BreakoutGame


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 86: RETRO BREAKOUT 2D ARCADE ENGINE & COLLISION PHYSICS")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Game Engine Architecture:")
    print("  • Vector Kinematics & Velocity Reflection on Wall Boundaries")
    print("  • Dynamic Angle Deflection: Paddle offset controls horizontal trajectory")
    print("  • Axis-Aligned Bounding Box (AABB) Multi-Row Brick Destruction")
    print("  • Score Progression & Lives State Machine")
    print("=" * 76 + "\n")


def run_ascii_arcade():
    """Runs a live autonomous demonstration where the paddle tracks the ball."""
    game = BreakoutGame()
    print("\n🕹️ RUNNING BREAKOUT AUTONOMOUS ARCADE SIMULATION")
    print("=" * 60)
    print("The paddle will automatically track the ball to demonstrate collision physics.\n")

    ticks = 0
    while ticks < 40:
        # Autonomous paddle tracking
        if game.paddle.x < game.ball.x - 10:
            game.paddle.move_right()
        elif game.paddle.x > game.ball.x + 10:
            game.paddle.move_left()

        status = game.step()
        ticks += 1

        if ticks % 4 == 0:
            print(f"--- Frame #{ticks} ---")
            print(game.render_ascii_frame())
            print()

        if status["game_over"] or status["won"]:
            break

    print(f"\nSimulation complete! Final Score: \033[92m{game.score} pts\033[0m | Remaining Bricks: {len([b for b in game.bricks if not b.is_destroyed])}")
    print("=" * 60 + "\n")


def launch_turtle_gui():
    """Launches graphical interactive Turtle Breakout if desktop display is accessible."""
    try:
        import turtle
        screen = turtle.Screen()
        screen.title("Breakout Arcade • Day 86")
        screen.bgcolor("#0f172a")
        screen.setup(width=600, height=600)
        screen.tracer(0)

        game = BreakoutGame(600, 600)

        # Paddle turtle
        pad_t = turtle.Turtle()
        pad_t.shape("square")
        pad_t.color("#38bdf8")
        pad_t.shapesize(stretch_wid=0.75, stretch_len=5.0)
        pad_t.penup()
        pad_t.goto(game.paddle.x, game.paddle.y)

        # Ball turtle
        ball_t = turtle.Turtle()
        ball_t.shape("circle")
        ball_t.color("#f59e0b")
        ball_t.penup()
        ball_t.goto(game.ball.x, game.ball.y)

        # Score turtle
        score_t = turtle.Turtle()
        score_t.color("#f8fafc")
        score_t.penup()
        score_t.hideturtle()
        score_t.goto(0, 260)
        score_t.write("Score: 0   Lives: 3", align="center", font=("Courier", 16, "bold"))

        # Controls
        screen.listen()
        screen.onkeypress(lambda: game.paddle.move_left(), "Left")
        screen.onkeypress(lambda: game.paddle.move_right(), "Right")
        screen.onkeypress(lambda: game.paddle.move_left(), "a")
        screen.onkeypress(lambda: game.paddle.move_right(), "d")

        for _ in range(300):
            status = game.step()
            pad_t.goto(game.paddle.x, game.paddle.y)
            ball_t.goto(game.ball.x, game.ball.y)
            screen.update()
            time.sleep(0.016)  # ~60 FPS
            if status["game_over"] or status["won"]:
                break

        screen.bye()
    except Exception as e:
        print(f"\n⚠️ Graphical display mode unavailable in current console environment: {e}")
        print("Running high-speed terminal simulation instead:")
        run_ascii_arcade()


def run_automated_tests():
    """Verifies ball movement, wall reflection, paddle bounce, and brick destruction."""
    print("\n🔍 Running Day 86 Automated Breakout Engine Verification Suite...")
    print("-" * 70)
    game = BreakoutGame()

    # 1. Initial State
    assert len(game.bricks) == 36, f"Expected 36 bricks, got {len(game.bricks)}"
    assert game.lives == 3
    assert game.score == 0
    print(" [PASS] 1. Brick matrix initialization: 36 destructible bricks initialized across 4 rows.")

    # 2. Ball Kinematics
    init_x, init_y = game.ball.x, game.ball.y
    game.ball.update()
    assert game.ball.x == init_x + game.ball.dx
    assert game.ball.y == init_y + game.ball.dy
    print(" [PASS] 2. 2D vector kinematics: Velocity updates position along (dx, dy).")

    # 3. Wall Bounce
    game.ball.x = game.half_w
    game.ball.dx = 5.0
    game.step()
    assert game.ball.dx < 0, "Ball must bounce off right arena boundary."
    print(" [PASS] 3. Boundary collision physics: Horizontal velocity reflected upon wall impact.")

    # 4. Brick AABB Collision
    target_brick = game.bricks[0]
    game.ball.x = target_brick.x
    game.ball.y = target_brick.y
    initial_score = game.score
    game.step()
    assert target_brick.is_destroyed is True
    assert game.score > initial_score
    print(f" [PASS] 4. AABB Brick collision: Brick destroyed and +{target_brick.points} points awarded.")

    # 5. Paddle Deflection
    game.ball.x = game.paddle.x
    game.ball.y = game.paddle.y + 10
    game.ball.dy = -5.0
    game.step()
    assert game.ball.dy > 0, "Ball must reflect upward after striking paddle."
    print(" [PASS] 5. Paddle contact deflection: Vertical velocity inverted upward.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Breakout Arcade Physics Engine fully operational.\n")


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 🕹️ Run Autonomous Terminal Arcade Simulation")
        print("  2) 🖥️ Launch Interactive GUI (Turtle Engine)")
        print("  3) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  4) 🚪 Exit")
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            run_ascii_arcade()
        elif choice == "2":
            launch_turtle_gui()
        elif choice == "3":
            run_automated_tests()
        elif choice in ("4", "exit", "quit", "q"):
            print("\n👋 Game Over! Keep breaking bricks! 🕹️\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-4.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 86 gracefully... Goodbye!\n")
