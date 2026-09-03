import sys
import time
import turtle as t
from art import logo
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
    """Main execution entrypoint for Day 20 - Snake Game Part 1 (Movement & Controls Engine)."""
    print(logo)
    print("Welcome to Snake Game Part 1! 🐍🕹️\n")

    screen = t.Screen()
    screen.setup(width=850, height=650)
    screen.bgcolor("#1e1e2e")
    screen.title("Day 20 - Snake Game (Part 1: Animation & Control Engine)")

    # Turn off automatic screen refresh for smooth manual animations
    screen.tracer(0)

    # Draw visual boundary frame
    draw_arena_border()

    # Initialize Snake instance
    snake = Snake()

    # Controls instructions in console
    print("🕹️ Controls: Use Arrow Keys or [W, A, S, D] to steer!")
    print("✨ Close window to exit loop.\n")

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

    game_is_on = True

    try:
        while game_is_on:
            screen.update()
            time.sleep(0.13)  # Smooth game frame tick rate

            # Move snake forward continuous steps
            snake.move()

    except (t.Terminator, Exception):
        print("🎮 GUI window closed. Game loop exited cleanly.")
        return

    try:
        screen.exitonclick()
    except Exception:
        pass


if __name__ == "__main__":
    main()

