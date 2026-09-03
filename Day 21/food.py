import random
import turtle as t


class Food(t.Turtle):
    """Models food items with regular (pink) and rare bonus golden star food types."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.speed("fastest")
        self.is_bonus = False
        self.points = 1
        self.spawn_count = 0
        self.refresh()

    def refresh(self) -> None:
        """Relocates food to random grid-aligned coordinates and occasionally spawns golden bonus food."""
        self.spawn_count += 1
        random_x = random.randint(-18, 18) * 20
        random_y = random.randint(-13, 11) * 20
        self.goto(random_x, random_y)

        # 20% chance or every 5th food item spawns Bonus Golden Food (+3 points)
        if self.spawn_count > 1 and (random.random() < 0.20 or self.spawn_count % 5 == 0):
            self.is_bonus = True
            self.points = 3
            self.shape("turtle")  # Distinct golden turtle shape for bonus food
            self.shapesize(stretch_len=0.9, stretch_wid=0.9)
            self.color("#f9e2af")  # Vibrant warm golden yellow
        else:
            self.is_bonus = False
            self.points = 1
            self.shape("circle")
            self.shapesize(stretch_len=0.6, stretch_wid=0.6)
            self.color("#f38ba8")  # Vibrant Catppuccin pink

