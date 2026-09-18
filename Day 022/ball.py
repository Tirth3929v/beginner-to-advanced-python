import turtle as t


class Ball(t.Turtle):
    """Models the Pong ball handling 2D velocity vectors, bounces, speed scaling, and resets."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("#f38ba8")  # Catppuccin Pink ball color
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def move(self) -> None:
        """Updates ball coordinates according to velocity vector."""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self) -> None:
        """Inverts vertical Y direction upon wall collision."""
        self.y_move *= -1

    def bounce_x(self) -> None:
        """Inverts horizontal X direction upon paddle collision and increases ball speed."""
        self.x_move *= -1
        self.move_speed *= 0.9  # Accelerate ball speed by 10% on each paddle hit

    def reset_position(self) -> None:
        """Resets ball to screen center, reverses initial direction, and resets speed."""
        self.goto(0, 0)
        self.move_speed = 0.1
        self.bounce_x()
