import random
import turtle as t


class Food(t.Turtle):
    """Models the food item that appears randomly on screen for the snake to consume."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.6, stretch_wid=0.6)
        self.color("#f38ba8")  # Vibrant food accent color (Catppuccin Pink)
        self.speed("fastest")
        self.refresh()

    def refresh(self) -> None:
        """Relocates food to random grid-aligned coordinates within the expanded arena."""
        random_x = random.randint(-18, 18) * 20
        random_y = random.randint(-13, 11) * 20
        self.goto(random_x, random_y)
