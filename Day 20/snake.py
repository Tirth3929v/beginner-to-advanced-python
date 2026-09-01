import turtle as t

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    """Models the Snake body composed of Turtle object segments and directional controls."""

    def __init__(self):
        self.segments: list[t.Turtle] = []
        self.create_snake()
        self.head: t.Turtle = self.segments[0]

    def create_snake(self) -> None:
        """Instantiates the initial 3-segment snake body."""
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position: tuple[int, int]) -> None:
        """Adds a new square turtle segment to the snake body at the specified coordinates."""
        new_segment = t.Turtle("square")
        new_segment.color("#a6e3a1")  # Mint green snake color
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def move(self) -> None:
        """Moves each segment to the position of the preceding segment to maintain body cohesion."""
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self) -> None:
        """Turns snake North, preventing 180-degree self-reversal."""
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self) -> None:
        """Turns snake South, preventing 180-degree self-reversal."""
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self) -> None:
        """Turns snake West, preventing 180-degree self-reversal."""
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self) -> None:
        """Turns snake East, preventing 180-degree self-reversal."""
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
