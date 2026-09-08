import sys
import time
import turtle as t
from art import logo
from car_manager import CarManager
from player import Player
from scoreboard import Scoreboard

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def display_game_info() -> bool:
    """Displays ASCII art logo, game features, controls guide, and prompts user to start."""
    print(logo)
    print("Welcome to Turtle Crossing Capstone Game! 🐢🚗")
    print("─" * 78)
    print("📖 GAME RULES & FEATURES:")
    print("   🎯 Objective      : Guide your turtle safely across busy multi-lane highway traffic!")
    print("   🚩 Finish Line    : Reach the top of the canvas to complete the level.")
    print("   ⚡ Level Up       : Every successful crossing resets your position and accelerates car speeds!")
    print("   💥 Danger Zone    : Avoid colliding with any moving car (Game Over on impact).")
    print("─" * 78)
    print("🕹️ GAME CONTROLS:")
    print("   ⬆️  Forward  : [ Up Arrow ]   or [ W ]")
    print("   ⬇️  Backward : [ Down Arrow ] or [ S ]")
    print("   ⬅️  Left     : [ Left Arrow ] or [ A ]")
    print("   ➡️  Right    : [ Right Arrow ] or [ D ]")
    print("─" * 78)

    user_input = input("\n👉 Press [ENTER] to launch the game window (or type 'q' to exit): ").strip().lower()
    if user_input in ["q", "quit", "exit"]:
        print("\nExiting game... Goodbye! 👋\n")
        return False
    print("\n🚀 Launching Turtle Crossing Arcade Window... Have fun! 🎮\n")
    return True


def main():
    """Main execution entrypoint for Turtle Crossing Capstone Game."""
    if not display_game_info():
        return

    screen = t.Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("#1e1e2e")
    screen.title("Day 23 - Turtle Crossing Capstone")
    screen.tracer(0)

    # Instantiate game objects
    player = Player()
    car_manager = CarManager()
    scoreboard = Scoreboard()

    # Controls binding
    screen.listen()
    screen.onkey(player.go_up, "Up")
    screen.onkey(player.go_down, "Down")
    screen.onkey(player.go_left, "Left")
    screen.onkey(player.go_right, "Right")

    screen.onkey(player.go_up, "w")
    screen.onkey(player.go_down, "s")
    screen.onkey(player.go_left, "a")
    screen.onkey(player.go_right, "d")
    screen.onkey(player.go_up, "W")
    screen.onkey(player.go_down, "S")
    screen.onkey(player.go_left, "A")
    screen.onkey(player.go_right, "D")


    game_is_on = True
    try:
        while game_is_on:
            time.sleep(0.1)
            screen.update()

            car_manager.create_car()
            car_manager.move_cars()

            # 1. Detect collision with cars
            for car in car_manager.all_cars:
                if car.distance(player) < 20:
                    game_is_on = False
                    scoreboard.game_over()
                    screen.update()
                    break

            # 2. Detect successful finish line crossing
            if player.is_at_finish_line():
                player.go_to_start()
                car_manager.level_up()
                scoreboard.increase_level()

    except (t.Terminator, Exception):
        print("🎮 GUI window closed. Game loop exited cleanly.")
        return

    try:
        screen.exitonclick()
    except Exception:
        pass


if __name__ == "__main__":
    main()
