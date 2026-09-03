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
    """Draws a sleek colored boundary box around the playable area (850x650 window)."""
    border = t.Turtle()
    border.hideturtle()
    border.speed("fastest")
    border.penup()
    border.color("#45475a")  # Elegant dark slate border line
    border.pensize(4)
    border.goto(-390, 240)
    border.pendown()
    for _ in range(2):
        border.forward(780)
        border.right(90)
        border.forward(510)
        border.right(90)


def main():
    """Main execution entrypoint for Day 21 - Retro Snake Arcade Capstone Edition."""
    print(logo)
    print("Welcome to Retro Snake Arcade Capstone Edition! 🐍🕹️\n")

    screen = t.Screen()
    screen.setup(width=850, height=650)
    screen.bgcolor("#1e1e2e")
    screen.title("Day 21 - Retro Snake Arcade (Enhanced Capstone Edition)")

    screen.tracer(0)
    draw_arena_border()

    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

    print("🕹️ Controls: Use Arrow Keys or [W, A, S, D] to steer!")
    print("⭐ Bonus: Golden turtles award +3 bonus points!")
    print("⚡ Speed: Snake speeds up as your score increases!")
    print("🔄 Restart: Press [ R ] or [ SPACE ] when Game Over!")
    print("✨ Close window to exit loop.\n")

    game_state = {"is_on": True}

    def trigger_restart():
        """Callback to restart the game loop after Game Over."""
        if not game_state["is_on"]:
            snake.reset()
            food.refresh()
            scoreboard.reset_score()
            game_state["is_on"] = True
            run_game_loop()

    screen.listen()
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")

    screen.onkey(snake.up, "w")
    screen.onkey(snake.down, "s")
    screen.onkey(snake.left, "a")
    screen.onkey(snake.right, "d")

    screen.onkey(trigger_restart, "r")
    screen.onkey(trigger_restart, "R")
    screen.onkey(trigger_restart, "space")

    def run_game_loop():
        try:
            while game_state["is_on"]:
                screen.update()

                # Dynamic Speed Scaling: base sleep is 0.13s, speeds up slightly every score threshold down to 0.05s max
                speed_delay = max(0.05, 0.13 - (scoreboard.score * 0.003))
                time.sleep(speed_delay)

                snake.move()

                # 1. Detect collision with food (regular or golden bonus food)
                if snake.head.distance(food) < 18:
                    earned_points = food.points
                    # Extend snake segments based on food value
                    for _ in range(earned_points):
                        snake.extend()
                    scoreboard.increase_score(earned_points)
                    food.refresh()

                # 2. Detect collision with wall boundaries
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

                # 3. Detect collision with tail using Python list slicing (snake.segments[1:])
                for segment in snake.segments[1:]:
                    if snake.head.distance(segment) < 10:
                        game_state["is_on"] = False
                        scoreboard.game_over()
                        screen.update()
                        break

        except (t.Terminator, Exception):
            print("🎮 GUI window closed. Game loop exited cleanly.")
            return

    run_game_loop()

    try:
        screen.exitonclick()
    except Exception:
        pass


if __name__ == "__main__":
    main()

