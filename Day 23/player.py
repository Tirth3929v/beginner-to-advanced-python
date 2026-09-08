import turtle as t

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(t.Turtle):
    """Models the player turtle avatar navigating across traffic lanes."""

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("#a6e3a1")  # Vibrant mint green turtle
        self.penup()
        self.go_to_start()
        self.setheading(90)

    def go_up(self) -> None:
        """Moves player forward (North) by step distance."""
        self.forward(MOVE_DISTANCE)

    def go_down(self) -> None:
        """Moves player backward (South) by step distance if within bottom boundary."""
        if self.ycor() > -280:
            self.backward(MOVE_DISTANCE)

    def go_left(self) -> None:
        """Moves player West by step distance if within left boundary."""
        if self.xcor() > -280:
            new_x = self.xcor() - MOVE_DISTANCE
            self.goto(new_x, self.ycor())

    def go_right(self) -> None:
        """Moves player East by step distance if within right boundary."""
        if self.xcor() < 280:
            new_x = self.xcor() + MOVE_DISTANCE
            self.goto(new_x, self.ycor())

    def go_to_start(self) -> None:
        """Resets player position back to starting line."""
        self.goto(STARTING_POSITION)

    def is_at_finish_line(self) -> bool:
        """Returns True if player crosses top finish line boundary, False otherwise."""
        return self.ycor() > FINISH_LINE_Y
