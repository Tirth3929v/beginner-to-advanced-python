import turtle as t

FONT = ("Courier", 18, "bold")
GAME_OVER_FONT = ("Courier", 26, "bold")


class Scoreboard(t.Turtle):
    """Manages level progression tracking and Game Over banner rendering."""

    def __init__(self):
        super().__init__()
        self.level = 1
        self.color("#cdd6f4")
        self.penup()
        self.hideturtle()
        self.goto(-260, 260)
        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        """Clears and renders current level HUD at top left."""
        self.clear()
        self.goto(-260, 260)
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def increase_level(self) -> None:
        """Increments level count by 1 and updates HUD."""
        self.level += 1
        self.update_scoreboard()

    def game_over(self) -> None:
        """Renders GAME OVER banner in center of screen."""
        self.goto(0, 0)
        self.color("#f38ba8")
        self.write("GAME OVER 💀", align="center", font=GAME_OVER_FONT)
