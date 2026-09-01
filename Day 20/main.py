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


def main():
    """Main execution entrypoint for Snake Game (Part 1)."""
    print(logo)
    print("Welcome to Snake Game Part 1 - Animation & Movement Engine! 🐍🕹️\n")

    screen = t.Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("#1e1e2e")
    screen.title("Day 20 - Retro Snake Engine (Part 1)")
    
    # Turn off automatic screen refresh for zero-lag smooth animations
    screen.tracer(0)

    # Initialize Snake model instance
    snake = Snake()

    # Event bindings for arrow keys and WASD controls
    screen.listen()
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")

    screen.onkey(snake.up, "w")
    screen.onkey(snake.down, "s")
    screen.onkey(snake.left, "a")
    screen.onkey(snake.right, "d")

    print("🕹️ Controls: Use Arrow Keys or [W, A, S, D] to steer the snake!")
    print("✨ Close GUI window to exit loop.\n")

    game_is_on = True
    while game_is_on:
        # Manually refresh canvas frame
        screen.update()
        time.sleep(0.1)
        
        # Advance snake
        snake.move()

    screen.exitonclick()


if __name__ == "__main__":
    main()
