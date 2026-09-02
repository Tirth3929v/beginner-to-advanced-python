import turtle as t

ALIGNMENT = "center"
FONT = ("Courier", 16, "bold")
GAME_OVER_FONT = ("Courier", 26, "bold")
RESTART_FONT = ("Courier", 14, "bold")


class Scoreboard(t.Turtle):
    """Manages game score tracking, high score persistence, HUD display, and Game Over restart prompt."""

    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0
        self.color("#cdd6f4")  # High contrast crisp light text color
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        """Clears and renders current score and high score at top center of canvas."""
        self.clear()
        self.goto(0, 260)
        self.write(
            f"Score: {self.score}   |   High Score: {self.high_score}",
            align=ALIGNMENT,
            font=FONT,
        )

    def increase_score(self) -> None:
        """Increments score count by 1 and updates HUD display."""
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_scoreboard()

    def game_over(self) -> None:
        """Displays GAME OVER banner and Restart prompt in center of screen."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.update_scoreboard()

        self.goto(0, 30)
        self.color("#f38ba8")  # Highlight red color for Game Over text
        self.write("GAME OVER 💀", align=ALIGNMENT, font=GAME_OVER_FONT)

        self.goto(0, -20)
        self.color("#a6e3a1")  # Mint green color for restart prompt
        self.write("Press  [ R ]  or  [ SPACE ]  to Restart Game", align=ALIGNMENT, font=RESTART_FONT)

    def reset_score(self) -> None:
        """Resets current score to 0 and redraws score HUD."""
        self.score = 0
        self.color("#cdd6f4")
        self.update_scoreboard()
