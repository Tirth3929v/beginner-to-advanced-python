import sys
import time
import turtle as t
from art import logo
from food import Food
from scoreboard import Scoreboard
from snake import Snake

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def draw_arena_border() -> None:
    """Draws a sleek colored boundary box around the playable area (800x600 window)."""
    border = t.Turtle()
    border.hideturtle()
    border.speed("fastest")
    border.penup()
    border.color("#45475a")  # Elegant dark slate border line
    border.pensize(4)
    # Arena bounds: X (-390 to 390), Y (-270 to 240)
    border.goto(-390, 240)
    border.pendown()
    for _ in range(2):
        border.forward(780)
        border.right(90)
        border.forward(510)
        border.right(90)


def main():
    """Main execution entrypoint for Retro Snake Arcade Game."""
    print(logo)
    print("Welcome to Retro Snake Arcade Game! 🐍🕹️\n")

    screen = t.Screen()
    screen.setup(width=850, height=650)
    screen.bgcolor("#1e1e2e")
    screen.title("Day 20 - Retro Snake Arcade Engine")

    # Turn off automatic screen refresh for smooth animations
    screen.tracer(0)

    # Draw visual boundary frame
    draw_arena_border()

    # Initialize Snake, Food, and Scoreboard instances
    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

    # Controls instructions in console
    print("🕹️ Controls: Use Arrow Keys or [W, A, S, D] to steer!")
    print("🔄 Restart: Press [ R ] or [ SPACE ] when Game Over!")
    print("✨ Close window to exit loop.\n")

    game_state = {"is_on": True, "in_menu": False}

    def trigger_restart():
        """Callback to restart the game loop after Game Over."""
        if not game_state["is_on"]:
            snake.reset()
            food.refresh()
            scoreboard.reset_score()
            game_state["is_on"] = True
            run_game_loop()

    # Key Bindings
    screen.listen()
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")

    screen.onkey(snake.up, "w")
    screen.onkey(snake.down, "s")
    screen.onkey(snake.left, "a")
    screen.onkey(snake.right, "d")

    # Restart Key Bindings
    screen.onkey(trigger_restart, "r")
    screen.onkey(trigger_restart, "R")
    screen.onkey(trigger_restart, "space")

    def run_game_loop():
        try:
            while game_state["is_on"]:
                screen.update()
                # Game Speed: 0.13s pause gives smooth, highly responsive & comfortable controls
                time.sleep(0.13)

                # Move snake forward
                snake.move()

                # 1. Detect collision with food
                if snake.head.distance(food) < 18:
                    food.refresh()
                    snake.extend()
                    scoreboard.increase_score()

                # 2. Detect collision with wall boundaries
                # Boundary limits for 800x600 arena: X (-385 to 385), Y (-265 to 235)
                if (
                    snake.head.xcor() > 380
                    or snake.head.xcor() < -380
                    or snake.head.ycor() > 230
                    or snake.head.ycor() < -260
                ):
                    game_state["is_on"] = False
                    scoreboard.game_over()
                    screen.update()
                    break

                # 3. Detect collision with tail segments
                for segment in snake.segments[1:]:
                    if snake.head.distance(segment) < 10:
                        game_state["is_on"] = False
                        scoreboard.game_over()
                        screen.update()
                        break

        except (t.Terminator, Exception):
            print("🎮 GUI window closed. Game loop exited cleanly.")
            return

    # Start initial game loop
    run_game_loop()

    try:
        screen.exitonclick()
    except Exception:
        pass


if __name__ == "__main__":
    main()
