import random
import turtle as t
from art import finish_flag


def start_turtle_race():
    """Runs the interactive Turtle Race simulator with multiple Turtle object instances."""
    is_race_on = False
    screen = t.Screen()
    screen.setup(width=500, height=400)
    screen.title("Day 19 - Ultimate Turtle Grand Prix 🏁")
    screen.bgcolor("#181825")

    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    y_positions = [-70, -40, -10, 20, 50, 80]
    all_turtles = []

    # Take user bet via pop-up dialog or fallback CLI prompt
    user_bet = screen.textinput(
        title="Make your bet",
        prompt="Which turtle will win the race? Enter a color (red/orange/yellow/green/blue/purple):"
    )

    if user_bet:
        user_bet = user_bet.strip().lower()
        is_race_on = True

    # Instantiate 6 distinct Turtle instances
    for turtle_index in range(6):
        new_turtle = t.Turtle(shape="turtle")
        new_turtle.color(colors[turtle_index])
        new_turtle.penup()
        new_turtle.goto(x=-230, y=y_positions[turtle_index])
        all_turtles.append(new_turtle)

    # Draw Finish Line
    finish_line = t.Turtle()
    finish_line.hideturtle()
    finish_line.penup()
    finish_line.goto(x=220, y=-100)
    finish_line.setheading(90)
    finish_line.color("#cdd6f4")
    finish_line.pensize(3)
    finish_line.pendown()
    finish_line.forward(200)

    # Race Simulation Engine Loop
    while is_race_on:
        for turtle in all_turtles:
            # 230 is the finish line threshold (250 width - 20 turtle size)
            if turtle.xcor() > 220:
                is_race_on = False
                winning_color = turtle.pencolor()
                
                print(finish_flag)
                if winning_color == user_bet:
                    print(f"🎉 YOU WON! The {winning_color.capitalize()} turtle crossed the finish line first! 🏆\n")
                else:
                    print(f"❌ YOU LOST! The {winning_color.capitalize()} turtle won the race! (Your bet: {user_bet})\n")
                break

            # Move turtle forward by a random distance step
            random_distance = random.randint(1, 10)
            turtle.forward(random_distance)

    screen.exitonclick()


if __name__ == "__main__":
    start_turtle_race()
