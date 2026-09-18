"""
Day 88: Todo List Web Application Server
Full-stack task productivity manager with Flask, SQLAlchemy, and REST API.
"""

import os
import sys
from typing import Optional
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Task

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def create_app(test_config: Optional[dict] = None) -> Flask:
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(os.path.join(base_dir, "instance"), exist_ok=True)

    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "todo-secret-key-day88")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'instance', 'tasks_day88.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    def seed_tasks():
        with app.app_context():
            db.create_all()
            if db.session.execute(db.select(Task)).first() is None:
                initial_tasks = [
                    Task(title="Complete #100DaysOfCode Python Curriculum", category="Study", priority="High", is_completed=True),
                    Task(title="Deploy Portfolio Web App to Production", category="Work", priority="High", is_completed=False),
                    Task(title="Refactor Multivariable ML Model Pipeline", category="Work", priority="Medium", is_completed=False),
                    Task(title="Read 25 pages of Software Architecture", category="Study", priority="Medium", is_completed=True),
                    Task(title="30-minute cardio workout & stretch", category="Health", priority="Low", is_completed=False),
                ]
                db.session.add_all(initial_tasks)
                db.session.commit()

    @app.route("/")
    def index():
        cat = request.args.get("cat", "").strip()
        if cat:
            tasks = db.session.execute(db.select(Task).where(Task.category == cat).order_by(Task.id.desc())).scalars().all()
        else:
            tasks = db.session.execute(db.select(Task).order_by(Task.id.desc())).scalars().all()

        total = len(tasks)
        completed = sum(1 for t in tasks if t.is_completed)
        progress_pct = int((completed / total * 100)) if total > 0 else 0

        return render_template(
            "index.html",
            tasks=tasks,
            selected_cat=cat,
            completed_count=completed,
            progress_pct=progress_pct
        )

    @app.route("/add", methods=["POST"])
    def add_task():
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "General").strip()
        priority = request.form.get("priority", "Medium").strip()
        if title:
            new_task = Task(title=title, category=category, priority=priority)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for("index"))

    @app.route("/toggle/<int:task_id>")
    def toggle_task(task_id: int):
        task = db.session.get(Task, task_id)
        if task:
            task.is_completed = not task.is_completed
            db.session.commit()
        return redirect(request.referrer or url_for("index"))

    @app.route("/delete/<int:task_id>")
    def delete_task(task_id: int):
        task = db.session.get(Task, task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return redirect(request.referrer or url_for("index"))

    @app.route("/api/tasks", methods=["GET", "POST"])
    def api_tasks():
        if request.method == "POST":
            data = request.get_json() or {}
            task = Task(
                title=data.get("title", "Untitled"),
                category=data.get("category", "General"),
                priority=data.get("priority", "Medium")
            )
            db.session.add(task)
            db.session.commit()
            return jsonify(task.to_dict()), 201
        tasks = db.session.execute(db.select(Task)).scalars().all()
        return jsonify([t.to_dict() for t in tasks])

    seed_tasks()
    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 Todo Desk web server running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
