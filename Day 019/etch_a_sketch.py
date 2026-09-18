import turtle as t


def move_forwards(tim: t.Turtle):
    tim.forward(10)


def move_backwards(tim: t.Turtle):
    tim.backward(10)


def turn_left(tim: t.Turtle):
    tim.left(10)


def turn_right(tim: t.Turtle):
    tim.right(10)


def clear_screen(tim: t.Turtle, screen: t.TurtleScreen):
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()


def run_etch_a_sketch():
    """Launches the interactive Etch-a-Sketch application with keyboard controls."""
    screen = t.Screen()
    screen.title("Day 19 - Etch-A-Sketch Studio")
    screen.bgcolor("#1e1e2e")

    tim = t.Turtle()
    tim.shape("turtle")
    tim.color("#89b4fa")
    tim.pensize(3)
    tim.speed("fastest")

    screen.listen()

    # Event binding using higher-order functions & lambdas
    screen.onkey(key="w", fun=lambda: move_forwards(tim))
    screen.onkey(key="s", fun=lambda: move_backwards(tim))
    screen.onkey(key="a", fun=lambda: turn_left(tim))
    screen.onkey(key="d", fun=lambda: turn_right(tim))
    screen.onkey(key="c", fun=lambda: clear_screen(tim, screen))

    print("\n✏️  Etch-A-Sketch controls:")
    print("   [W] Forwards | [S] Backwards | [A] Turn Counter-Clockwise | [D] Turn Clockwise | [C] Clear")
    print("✨ Click canvas window to exit.")

    screen.exitonclick()


if __name__ == "__main__":
    run_etch_a_sketch()
