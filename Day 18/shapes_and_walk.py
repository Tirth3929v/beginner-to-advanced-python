import random
import turtle as t

# Curated vibrant RGB palette tuples
COLOR_PALETTE = [
    (245, 66, 66),   # Coral Red
    (245, 141, 66),  # Vibrant Orange
    (245, 215, 66),  # Golden Yellow
    (66, 245, 108),  # Bright Emerald
    (66, 203, 245),  # Sky Blue
    (66, 81, 245),   # Royal Blue
    (170, 66, 245),  # Purple
    (245, 66, 191),  # Magenta
]


def setup_screen(title: str):
    """Sets up the Turtle canvas window with custom dimensions and RGB colormode."""
    screen = t.Screen()
    screen.title(title)
    screen.bgcolor("#1e1e2e")  # Dark sleek background
    t.colormode(255)
    return screen


def draw_geometric_shapes():
    """Draws overlapping regular polygons from triangle (3 sides) to decagon (10 sides)."""
    screen = setup_screen("Day 18 - Geometric Polygons Drawer")
    timmy = t.Turtle()
    timmy.shape("turtle")
    timmy.pensize(3)
    timmy.speed(8)

    # Position turtle
    timmy.penup()
    timmy.goto(-50, -100)
    timmy.pendown()

    for sides in range(3, 11):
        color = random.choice(COLOR_PALETTE)
        timmy.pencolor(color)
        angle = 360 / sides
        for _ in range(sides):
            timmy.forward(100)
            timmy.right(angle)

    timmy.hideturtle()
    print("✨ Geometric Polygons generated! Close window to continue.")
    screen.exitonclick()


def draw_random_walk(steps: int = 200):
    """Generates a randomized 2D random walk with changing RGB colors and thick pen strokes."""
    screen = setup_screen("Day 18 - 2D Random Walk Generator")
    timmy = t.Turtle()
    timmy.shape("turtle")
    timmy.pensize(8)
    timmy.speed(0)  # Fastest speed

    directions = [0, 90, 180, 270]

    for _ in range(steps):
        timmy.pencolor(random.choice(COLOR_PALETTE))
        timmy.forward(30)
        timmy.setheading(random.choice(directions))

    timmy.hideturtle()
    print("✨ Random Walk pattern generated! Close window to continue.")
    screen.exitonclick()


if __name__ == "__main__":
    draw_geometric_shapes()
