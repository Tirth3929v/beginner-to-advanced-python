"""
Day 54: First Flask Web Application
Demonstrates routing with @app.route decorators and dynamic responses.
"""

from flask import Flask
from decorator_playground import make_bold, make_emphasis, make_underlined

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Day 54: Hello Flask!</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding: 60px 20px; }
            .card { background: #1e293b; max-width: 600px; margin: 0 auto; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
            h1 { color: #38bdf8; font-size: 2.2rem; }
            p { color: #94a3b8; font-size: 1.1rem; line-height: 1.6; }
            a { color: #38bdf8; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
            .nav { margin-top: 30px; display: flex; justify-content: center; gap: 20px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Hello, World! Welcome to Flask</h1>
            <p>You have successfully launched your Day 54 Flask micro-service powered by Python function decorators!</p>
            <div class="nav">
                <a href="/bye">👋 /bye</a>
                <a href="/greet/Developer">👋 /greet/Developer</a>
                <a href="/status">📊 /status</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "Goodbye and happy coding with Flask decorators!"


@app.route("/greet/<name>")
def greet_user(name):
    return f"""
    <div style="text-align:center; padding: 50px; font-family: sans-serif; background: #0f172a; color: #38bdf8; min-height: 100vh;">
        <h2>✨ Welcome, {name.title()}!</h2>
        <p style="color: #94a3b8;">Dynamic route parsed with <code>&lt;name&gt;</code> path variable.</p>
        <p><a href="/" style="color: #38bdf8;">⬅️ Return Home</a></p>
    </div>
    """


@app.route("/status")
def status():
    return {"status": "online", "framework": "Flask 3.x", "day": 54, "architecture": "Decorated Microservice"}


if __name__ == "__main__":
    print("🌐 Starting Day 54 Flask Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
