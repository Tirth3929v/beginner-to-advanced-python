import math
import sys
import tkinter as tk

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------------------------- CONSTANTS & COLOR PALETTE ------------------------------- #
PINK = "#f38ba8"
RED = "#e78284"
GREEN = "#a6e3a1"
YELLOW = "#f9e2af"
TEAL = "#94e2d5"
BG_DARK = "#1e1e2e"
SURFACE = "#313244"
TEXT_COLOR = "#cdd6f4"
FONT_NAME = "Courier"

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20


class PomodoroTimerApp:
    """Tkinter Pomodoro Desktop Application with Canvas vector rendering and event scheduling."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pomodoro Focus Studio 🍅")
        self.window.config(padx=40, pady=30, bg=BG_DARK)
        self.window.resizable(False, False)

        self.reps = 0
        self.timer = None
        self.is_running = False

        self.setup_ui()

    def setup_ui(self):
        # 1. Main Title Label
        self.title_label = tk.Label(
            self.window,
            text="Timer",
            font=(FONT_NAME, 36, "bold"),
            fg=GREEN,
            bg=BG_DARK
        )
        self.title_label.grid(column=1, row=0, pady=(0, 15))

        # 2. Canvas with Vector Tomato Graphics
        self.canvas = tk.Canvas(self.window, width=220, height=224, bg=BG_DARK, highlightthickness=0)
        
        # Tomato Leaves (green stem & leaves)
        self.canvas.create_polygon(110, 40, 90, 20, 105, 30, fill=GREEN, outline=GREEN)
        self.canvas.create_polygon(110, 40, 130, 20, 115, 30, fill=GREEN, outline=GREEN)
        self.canvas.create_line(110, 40, 110, 15, width=4, fill="#89b4fa")
        
        # Tomato Body (rich vibrant red oval)
        self.canvas.create_oval(25, 35, 195, 195, fill=RED, outline="#ea999c", width=2)
        
        # Highlights for 3D depth
        self.canvas.create_oval(45, 55, 75, 85, fill="#ea999c", outline="")

        # Dynamic Timer Text
        self.timer_text = self.canvas.create_text(
            110, 120,
            text="25:00",
            fill="#ffffff",
            font=(FONT_NAME, 30, "bold")
        )
        self.canvas.grid(column=1, row=1)

        # 3. Start Button
        self.start_button = tk.Button(
            self.window,
            text="Start",
            font=(FONT_NAME, 12, "bold"),
            bg=GREEN,
            fg="#11111b",
            activebackground="#94e2d5",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.start_timer
        )
        self.start_button.grid(column=0, row=2, padx=10, pady=20)

        # 4. Reset Button
        self.reset_button = tk.Button(
            self.window,
            text="Reset",
            font=(FONT_NAME, 12, "bold"),
            bg=PINK,
            fg="#11111b",
            activebackground="#ea999c",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.reset_timer
        )
        self.reset_button.grid(column=2, row=2, padx=10, pady=20)

        # 5. Checkmarks Label
        self.check_marks = tk.Label(
            self.window,
            text="",
            font=(FONT_NAME, 16, "bold"),
            fg=GREEN,
            bg=BG_DARK
        )
        self.check_marks.grid(column=1, row=3)

    def reset_timer(self):
        """Cancels active timer callback, resets reps and returns UI to default state."""
        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

        self.canvas.itemconfig(self.timer_text, text="25:00")
        self.title_label.config(text="Timer", fg=GREEN)
        self.check_marks.config(text="")
        self.reps = 0
        self.is_running = False

    def start_timer(self):
        """Starts countdown for the current Pomodoro cycle stage."""
        if self.is_running:
            return  # Prevent multiple simultaneous timer schedules

        self.is_running = True
        self.reps += 1

        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if self.reps % 8 == 0:
            self.count_down(long_break_sec)
            self.title_label.config(text="Break 🌴", fg=RED)
            try:
                self.window.bell()
            except Exception:
                pass
        elif self.reps % 2 == 0:
            self.count_down(short_break_sec)
            self.title_label.config(text="Break ☕", fg=PINK)
            try:
                self.window.bell()
            except Exception:
                pass
        else:
            self.count_down(work_sec)
            self.title_label.config(text="Work 💻", fg=GREEN)

    def count_down(self, count):
        """Recursive timer callback using window.after() with dynamic formatting."""
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"

        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")

        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            self.is_running = False
            self.start_timer()
            # Update checkmarks for completed work sessions (each work session = 2 reps)
            marks = ""
            work_sessions = math.floor(self.reps / 2)
            for _ in range(work_sessions):
                marks += "✔ "
            self.check_marks.config(text=marks)

    def run(self):
        """Launches the Tkinter event loop."""
        self.window.mainloop()


def start_pomodoro_app():
    app = PomodoroTimerApp()
    app.run()


if __name__ == "__main__":
    start_pomodoro_app()
