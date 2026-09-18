import turtle as t


class Paddle(t.Turtle):
    """Models a player paddle object inheriting from Turtle for movement controls."""

    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.shape("square")
        self.color("#cdd6f4")
        self.shapesize(stretch_wid=5, stretch_len=1)  # 100px height by 20px width
        self.penup()
        self.goto(position)

    def go_up(self) -> None:
        """Moves paddle up by 20px, staying within top screen boundary."""
        if self.ycor() < 240:
            new_y = self.ycor() + 20
            self.goto(self.xcor(), new_y)

    def go_down(self) -> None:
        """Moves paddle down by 20px, staying within bottom screen boundary."""
        if self.ycor() > -240:
            new_y = self.ycor() - 20
            self.goto(self.xcor(), new_y)
