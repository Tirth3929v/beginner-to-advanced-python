import random
import turtle as t

# Damien Hirst inspired color palette (RGB tuples extracted from fine art)
HIRST_PALETTE = [
    (235, 76, 52),   # Vermilion
    (240, 168, 48),  # Warm Amber
    (245, 224, 66),  # Sunburst Yellow
    (75, 196, 99),   # Mint Green
    (48, 147, 217),  # Azure Blue
    (115, 68, 209),  # Amethyst Purple
    (219, 57, 146),  # Deep Magenta
    (41, 186, 172),  # Teal
    (230, 115, 50),  # Burnt Orange
    (70, 70, 70),    # Slate Charcoal
]


def generate_hirst_painting(grid_size: int = 10, dot_radius: int = 20, spacing: int = 50):
    """Generates a 10x10 Damien Hirst style spot painting on canvas using Turtle graphics."""
    screen = t.Screen()
    screen.title("Day 18 - Damien Hirst Spot Painting Generator")
    screen.bgcolor("#fafafa")
    t.colormode(255)

    artist = t.Turtle()
    artist.shape("turtle")
    artist.speed(0)
    artist.penup()
    artist.hideturtle()

    # Calculate starting offsets to center the grid
    start_x = -((grid_size - 1) * spacing) / 2
    start_y = -((grid_size - 1) * spacing) / 2
    artist.setposition(start_x, start_y)

    print(f"🎨 Generating {grid_size}x{grid_size} Hirst Spot Painting...")

    for row in range(grid_size):
        for col in range(grid_size):
            color = random.choice(HIRST_PALETTE)
            artist.dot(dot_radius, color)
            if col < grid_size - 1:
                artist.forward(spacing)

        # Move up to next row and reset x position
        artist.setposition(start_x, start_y + (row + 1) * spacing)

    print("✨ Hirst Spot Painting Complete! Click canvas window to exit.")
    screen.exitonclick()


if __name__ == "__main__":
    generate_hirst_painting()
