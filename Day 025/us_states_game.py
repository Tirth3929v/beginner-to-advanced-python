import csv
import os
import sys
import turtle as t

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATES_CSV = os.path.join(BASE_DIR, "50_states.csv")
LEARN_CSV = os.path.join(BASE_DIR, "states_to_learn.csv")


def load_states_data() -> dict[str, tuple[int, int]]:
    """Loads 50 U.S. states data and map coordinates into a dictionary lookup."""
    states_dict = {}
    if not os.path.exists(STATES_CSV):
        return states_dict

    try:
        import pandas as pd
        df = pd.read_csv(STATES_CSV)
        for _, row in df.iterrows():
            states_dict[str(row["state"]).strip().title()] = (int(row["x"]), int(row["y"]))
    except Exception:
        with open(STATES_CSV, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row["state"].strip().title()
                states_dict[name] = (int(row["x"]), int(row["y"]))
    return states_dict


def run_us_states_game():
    """Launches the 50 U.S. States guessing game engine with coordinate plotting."""
    states_dict = load_states_data()
    all_states = list(states_dict.keys())
    guessed_states: list[str] = []

    print("\n🗺️  Launching U.S. States Map Game...")
    print("   Type state names into the prompt to place them on the canvas.")
    print("   Type 'Exit' to finish and save missing states to 'states_to_learn.csv'.\n")

    screen = t.Screen()
    screen.setup(width=720, height=550)
    screen.title("Day 25 - U.S. States Quiz Game 🗺️")
    screen.bgcolor("#181825")

    # Draw Map Border & Title
    writer = t.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("#cdd6f4")

    while len(guessed_states) < 50:
        score_text = f"{len(guessed_states)}/50 States Correct"
        answer_state = screen.textinput(
            title=score_text,
            prompt="What's another state's name? (or type 'Exit' to quit):"
        )

        if not answer_state:
            break

        guess = answer_state.strip().title()

        if guess == "Exit":
            # Save missed states to learn
            missing_states = [state for state in all_states if state not in guessed_states]
            with open(LEARN_CSV, mode="w", newline="", encoding="utf-8") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(["State"])
                for s in missing_states:
                    csv_writer.writerow([s])
            print(f"📝 Saved {len(missing_states)} missed states to '{LEARN_CSV}'!")
            break

        if guess in states_dict and guess not in guessed_states:
            guessed_states.append(guess)
            x, y = states_dict[guess]
            writer.goto(x, y)
            writer.write(guess, align="center", font=("Courier", 10, "bold"))
            print(f"  ✅ Correct! Placed '{guess}' at ({x}, {y}). Score: {len(guessed_states)}/50")

    print(f"\n🎉 Game Over! Final Score: {len(guessed_states)}/50\n")
    try:
        screen.exitonclick()
    except Exception:
        pass


if __name__ == "__main__":
    run_us_states_game()
