"""
Day 34 - QuizInterface Desktop GUI
Built with Tkinter Canvas, score HUD, True/False buttons,
and 1000ms color-feedback transition timer.
"""

import tkinter as tk
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
WHITE = "#FFFFFF"
CORRECT_GREEN = "#51CF66"
WRONG_RED = "#FF6B6B"


class QuizInterface:
    """Tkinter Desktop User Interface for Quizzer App."""

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = tk.Tk()
        self.window.title("Quizzler - Trivia Knowledge App 🧠🏆")
        self.window.config(padx=25, pady=25, bg=THEME_COLOR)
        self.window.resizable(False, False)

        # 1. Score Label HUD
        self.score_label = tk.Label(
            self.window,
            text=f"Score: {self.quiz.score}/{len(self.quiz.question_list)}",
            font=("Arial", 12, "bold"),
            fg=WHITE,
            bg=THEME_COLOR
        )
        self.score_label.grid(row=0, column=1, sticky="e", pady=(0, 15))

        # 2. Question Canvas Card
        self.canvas = tk.Canvas(self.window, width=320, height=260, bg=WHITE, highlightthickness=0)
        self.question_text = self.canvas.create_text(
            160, 130,
            width=280,
            text="Question placeholder text",
            fill=THEME_COLOR,
            font=("Arial", 13, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # 3. True Button (Green)
        self.true_btn = tk.Button(
            self.window,
            text="✔️ TRUE",
            font=("Arial", 14, "bold"),
            bg=CORRECT_GREEN,
            fg=WHITE,
            activebackground="#40C057",
            activeforeground=WHITE,
            width=10,
            pady=10,
            relief="flat",
            cursor="hand2",
            command=self.true_pressed
        )
        self.true_btn.grid(row=2, column=0, padx=(0, 10))

        # 4. False Button (Red)
        self.false_btn = tk.Button(
            self.window,
            text="✖️ FALSE",
            font=("Arial", 14, "bold"),
            bg=WRONG_RED,
            fg=WHITE,
            activebackground="#FA5252",
            activeforeground=WHITE,
            width=10,
            pady=10,
            relief="flat",
            cursor="hand2",
            command=self.false_pressed
        )
        self.false_btn.grid(row=2, column=1, padx=(10, 0))

        # Keyboard shortcuts
        self.window.bind("<t>", lambda _: self.true_pressed())
        self.window.bind("<f>", lambda _: self.false_pressed())
        self.window.bind("<Left>", lambda _: self.true_pressed())
        self.window.bind("<Right>", lambda _: self.false_pressed())

        self.get_next_question()

    def get_next_question(self):
        """Advances to the next question or finishes quiz."""
        self.canvas.config(bg=WHITE)
        self.true_btn.config(state="normal")
        self.false_btn.config(state="normal")

        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}/{len(self.quiz.question_list)}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text, fill=THEME_COLOR)
        else:
            self.canvas.itemconfig(
                self.question_text,
                text=f"🎉 Quiz Complete!\n\nYour Final Score:\n{self.quiz.score} / {len(self.quiz.question_list)}",
                fill=THEME_COLOR
            )
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right: bool):
        """Flashes canvas green/red for 1000ms, then advances."""
        self.true_btn.config(state="disabled")
        self.false_btn.config(state="disabled")

        if is_right:
            self.canvas.config(bg=CORRECT_GREEN)
            self.canvas.itemconfig(self.question_text, fill=WHITE)
        else:
            self.canvas.config(bg=WRONG_RED)
            self.canvas.itemconfig(self.question_text, fill=WHITE)

        self.window.after(1000, self.get_next_question)

    def run(self):
        self.window.mainloop()
