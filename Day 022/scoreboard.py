import turtle as t

ALIGNMENT = "center"
FONT = ("Courier", 40, "bold")


class Scoreboard(t.Turtle):
    """Manages player scores, net rendering, and score HUD for Pong Arcade."""

    def __init__(self):
        super().__init__()
        self.color("#cdd6f4")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.draw_net()
        self.update_scoreboard()

    def draw_net(self) -> None:
        """Draws a dashed vertical center net line."""
        net = t.Turtle()
        net.hideturtle()
        net.color("#45475a")
        net.pensize(4)
        net.penup()
        net.goto(0, -290)
        net.setheading(90)
        while net.ycor() < 290:
            net.pendown()
            net.forward(15)
            net.penup()
            net.forward(15)

    def update_scoreboard(self) -> None:
        """Renders current left and right player scores."""
        self.clear()
        self.goto(-100, 220)
        self.write(self.l_score, align=ALIGNMENT, font=FONT)
        self.goto(100, 220)
        self.write(self.r_score, align=ALIGNMENT, font=FONT)

    def l_point(self) -> None:
        """Increments Left Player score by 1 point."""
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self) -> None:
        """Increments Right Player score by 1 point."""
        self.r_score += 1
        self.update_scoreboard()
