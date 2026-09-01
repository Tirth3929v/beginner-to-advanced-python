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


def setup_screen(title: str, width: int = 750, height: int = 750):
    """Sets up and clears the Turtle canvas window with custom dimensions and RGB colormode."""
    screen = t.Screen()
    screen.clearscreen()
    screen.setup(width=width, height=height)
    screen.title(title)
    screen.bgcolor("#1e1e2e")  # Dark sleek background
    t.colormode(255)
    return screen


def draw_geometric_shapes():
    """Draws upright, overlapping regular polygons from triangle (3 sides) to decagon (10 sides)."""
    screen = setup_screen("Day 18 - Geometric Polygons Drawer")
    timmy = t.Turtle()
    timmy.shape("turtle")
    timmy.pensize(3)
    timmy.speed(8)

    # Position turtle at base center so all shapes draw upright and perfectly centered
    timmy.penup()
    timmy.goto(-40, -140)
    timmy.setheading(0)
    timmy.pendown()

    for sides in range(3, 11):
        color = random.choice(COLOR_PALETTE)
        timmy.pencolor(color)
        angle = 360 / sides
        for _ in range(sides):
            timmy.forward(80)
            timmy.left(angle)

    timmy.hideturtle()
    print("✨ Geometric Polygons generated! Close window to continue.")
    screen.exitonclick()


def draw_random_walk(steps: int = 200):
    """Generates a centered, bounded 2D random walk with changing RGB colors and thick pen strokes."""
    screen = setup_screen("Day 18 - 2D Random Walk Generator")
    timmy = t.Turtle()
    timmy.shape("turtle")
    timmy.pensize(8)
    timmy.speed(0)  # Fastest speed

    directions = [0, 90, 180, 270]

    for _ in range(steps):
        timmy.pencolor(random.choice(COLOR_PALETTE))
        
        # Keep walk bounded within screen to stay visually centered
        if abs(timmy.xcor()) > 300 or abs(timmy.ycor()) > 300:
            timmy.setheading(timmy.towards(0, 0))
        else:
            timmy.setheading(random.choice(directions))
            
        timmy.forward(30)

    timmy.hideturtle()
    print("✨ Random Walk pattern generated! Close window to continue.")
    screen.exitonclick()


def draw_spirograph(gap_size: int = 5, radius: int = 100):
    """Generates a centered, multi-colored Spirograph pattern using overlapping circles."""
    screen = setup_screen("Day 18 - Spirograph Generator")
    timmy = t.Turtle()
    timmy.shape("turtle")
    timmy.pensize(2)
    timmy.speed(0)

    for _ in range(int(360 / gap_size)):
        timmy.pencolor(random.choice(COLOR_PALETTE))
        timmy.circle(radius)
        timmy.setheading(timmy.heading() + gap_size)

    timmy.hideturtle()
    print("✨ Spirograph pattern generated! Close window to continue.")
    screen.exitonclick()


if __name__ == "__main__":
    draw_geometric_shapes()

