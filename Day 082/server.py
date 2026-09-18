"""
Day 82: Portfolio Website Application Server
Serves personal developer showcase with Flask, Jinja2, and responsive design.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from portfolio_data import PROFILE

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "portfolio-dev-secret-key-day82")

    @app.route("/", methods=["GET", "POST"])
    def index():
        message_sent = False
        if request.method == "POST":
            # Simulate receiving contact message
            message_sent = True
        return render_template("index.html", profile=PROFILE, message_sent=message_sent)

    @app.route("/api/projects")
    def api_projects():
        return jsonify(PROFILE["projects"])

    @app.route("/api/skills")
    def api_skills():
        return jsonify(PROFILE["skills"])

    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 Portfolio website running at: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
