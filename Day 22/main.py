import sys
import time
import turtle as t
from art import logo
from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main execution entrypoint for Pong Arcade Game (Day 22)."""
    print(logo)
    print("Welcome to The Famous Pong Arcade Game! 🏓🕹️\n")

    screen = t.Screen()
    screen.bgcolor("#1e1e2e")
    screen.setup(width=800, height=600)
    screen.title("Day 22 - Pong Arcade Engine")
    screen.tracer(0)

    # Instantiate game objects
    r_paddle = Paddle((350, 0))
    l_paddle = Paddle((-350, 0))
    ball = Ball()
    scoreboard = Scoreboard()

    # Bind player controls
    screen.listen()
    screen.onkey(r_paddle.go_up, "Up")
    screen.onkey(r_paddle.go_down, "Down")
    screen.onkey(l_paddle.go_up, "w")
    screen.onkey(l_paddle.go_down, "s")
    screen.onkey(l_paddle.go_up, "W")
    screen.onkey(l_paddle.go_down, "S")

    print("🕹️ Controls:")
    print("   Player 1 (Left) : [W] Up | [S] Down")
    print("   Player 2 (Right): [Up Arrow] Up | [Down Arrow] Down")
    print("✨ Close GUI window to exit loop.\n")

    game_is_on = True
    try:
        while game_is_on:
            time.sleep(ball.move_speed)
            screen.update()
            ball.move()

            # 1. Detect top & bottom wall bounce
            if ball.ycor() > 280 or ball.ycor() < -280:
                ball.bounce_y()

            # 2. Detect collision with right & left paddles
            if (
                ball.distance(r_paddle) < 50 and ball.xcor() > 320
                or ball.distance(l_paddle) < 50 and ball.xcor() < -320
            ):
                ball.bounce_x()

            # 3. Detect Right paddle miss (Left player scores point)
            if ball.xcor() > 380:
                ball.reset_position()
                scoreboard.l_point()

            # 4. Detect Left paddle miss (Right player scores point)
            if ball.xcor() < -380:
                ball.reset_position()
                scoreboard.r_point()

    except (t.Terminator, Exception):
        print("🎮 GUI window closed. Game loop exited cleanly.")
        return

    try:
        screen.exitonclick()
    except Exception:
        pass


if __name__ == "__main__":
    main()
