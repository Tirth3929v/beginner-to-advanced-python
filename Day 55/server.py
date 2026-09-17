"""
Day 55: Higher or Lower Number Guessing Flask Web Game
Parses URL path variables (<int:guess>) and renders dynamic HTML/Giphy responses.
"""

import random
from flask import Flask

app = Flask(__name__)

# Generate random secret number between 0 and 9
secret_number = random.randint(0, 9)


def get_secret() -> int:
    return secret_number


def reset_secret() -> int:
    global secret_number
    secret_number = random.randint(0, 9)
    return secret_number


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 55: Higher or Lower Game</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            text-align: center;
            padding: 40px 20px;
            margin: 0;
        }}
        .container {{
            max-width: 650px;
            margin: 0 auto;
            background: #1e293b;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }}
        h1 {{ color: {color}; margin-bottom: 10px; }}
        p {{ color: #94a3b8; font-size: 1.1rem; line-height: 1.5; }}
        img {{ border-radius: 12px; margin: 20px 0; max-width: 100%; height: auto; }}
        .buttons {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 25px; }}
        .btn {{
            background: #334155;
            color: #38bdf8;
            padding: 10px 18px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1rem;
            transition: all 0.2s ease;
        }}
        .btn:hover {{ background: #38bdf8; color: #0f172a; transform: translateY(-2px); }}
        .reset-btn {{ background: #ef4444; color: white; }}
        .reset-btn:hover {{ background: #dc2626; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p>{subtitle}</p>
        <img src="{gif_url}" alt="Game Feedback" width="400">
        <p>Quick Click or enter <code>/&lt;number&gt;</code> in your browser address bar:</p>
        <div class="buttons">
            {buttons}
        </div>
    </div>
</body>
</html>
"""


def render_page(title: str, subtitle: str, color: str, gif_url: str) -> str:
    btn_links = "".join([f'<a class="btn" href="/{i}">{i}</a>' for i in range(10)])
    btn_links += '<a class="btn reset-btn" href="/reset">🔄 New Game</a>'
    return PAGE_TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        color=color,
        gif_url=gif_url,
        buttons=btn_links
    )


@app.route("/")
def home():
    return render_page(
        title="🎯 Guess a number between 0 and 9",
        subtitle="Can you read the server's mind? Pick a number below to test your intuition!",
        color="#38bdf8",
        gif_url="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"
    )


@app.route("/<int:guess>")
def check_guess(guess: int):
    if guess < 0 or guess > 9:
        return render_page(
            title="⚠️ Out of Bounds!",
            subtitle="Please pick an integer strictly between 0 and 9.",
            color="#f59e0b",
            gif_url="https://media.giphy.com/media/l2JehQ2GitHGdVG9y/giphy.gif"
        )
    elif guess < secret_number:
        return render_page(
            title="📉 Too low, try again!",
            subtitle=f"You guessed {guess}. The secret number is higher!",
            color="#ec4899",
            gif_url="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"
        )
    elif guess > secret_number:
        return render_page(
            title="📈 Too high, try again!",
            subtitle=f"You guessed {guess}. The secret number is lower!",
            color="#a855f7",
            gif_url="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"
        )
    else:
        return render_page(
            title="🎉 You found me! BINGO!",
            subtitle=f"Spot on! {guess} was the secret number! Amazing deduction skills.",
            color="#22c55e",
            gif_url="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"
        )


@app.route("/reset")
def reset_game():
    new_num = reset_secret()
    return render_page(
        title="🔄 Game Reset Successfully!",
        subtitle="A fresh secret number has been chosen. Make your guess!",
        color="#38bdf8",
        gif_url="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"
    )


if __name__ == "__main__":
    print(f"🎯 Server target secret number is: {secret_number}")
    print("🌐 Starting Day 55 Flask Game Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
