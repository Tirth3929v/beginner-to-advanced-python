import random
import turtle as t

COLORS = [
    "#f38ba8",  # Pink
    "#fab387",  # Peach / Orange
    "#f9e2af",  # Yellow
    "#a6e3a1",  # Mint
    "#89dceb",  # Sky Blue
    "#cba6f7",  # Lavender
    "#e5c890",  # Amber
]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 3


class CarManager:
    """Manages spawning, movement, and difficulty scaling of traffic car objects."""

    def __init__(self):
        self.all_cars: list[t.Turtle] = []
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_car(self) -> None:
        """Spawns a new car at random Y lane coordinates with 1-in-6 probability tick."""
        random_chance = random.randint(1, 6)
        if random_chance == 1:
            new_car = t.Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)  # 20px height by 40px width
            new_car.penup()
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-240, 240)
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)

    def move_cars(self) -> None:
        """Moves all active cars Westward across the canvas."""
        for car in self.all_cars:
            car.backward(self.car_speed)

    def level_up(self) -> None:
        """Increases car speed for next level."""
        self.car_speed += MOVE_INCREMENT
