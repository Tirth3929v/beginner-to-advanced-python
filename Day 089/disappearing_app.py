"""
Day 89: Disappearing Text Writing Application Engine
Enforces unbroken flow state by wiping buffer if typing stops for 5 seconds.
"""

import time
import os
from typing import Optional, Tuple


class WritingSession:
    def __init__(self, timeout_seconds: float = 5.0, goal_seconds: float = 60.0):
        self.timeout_seconds = timeout_seconds
        self.goal_seconds = goal_seconds
        self.buffer = ""
        self.last_keystroke_time = time.time()
        self.session_start_time = time.time()
        self.is_vanished = False
        self.is_completed = False

    def on_keystroke(self, current_text: str):
        """Called whenever user types a character."""
        if self.is_vanished:
            return
        self.buffer = current_text
        self.last_keystroke_time = time.time()

    def check_status(self, now: Optional[float] = None) -> Tuple[bool, float, str]:
        """
        Checks current time against timeout and goal.
        Returns: (is_active, seconds_left_before_disappearing, message)
        """
        current_t = time.time() if now is None else now
        elapsed_inactivity = current_t - self.last_keystroke_time
        total_writing_time = current_t - self.session_start_time

        # Check goal victory
        if total_writing_time >= self.goal_seconds and not self.is_vanished and len(self.buffer) > 0:
            self.is_completed = True
            return False, 0.0, "VICTORY! You maintained flow and achieved your writing goal."

        # Check timeout expiration
        if elapsed_inactivity >= self.timeout_seconds and not self.is_completed:
            self.buffer = ""
            self.is_vanished = True
            return False, 0.0, "VANISHED! You stopped typing for too long. All progress lost."

        remaining_inactivity = max(0.0, self.timeout_seconds - elapsed_inactivity)
        return True, remaining_inactivity, "Writing in progress..."

    def save_work(self, filename: str = "completed_writing.txt") -> Optional[str]:
        """Saves current buffer if goal was achieved."""
        if not self.buffer or self.is_vanished:
            return None
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.buffer)
        return path


def launch_tkinter_gui(timeout: int = 5, goal_seconds: int = 60):
    """Launches full graphical desktop interface with live fading text."""
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.title("Disappearing Text Writing App • Flow State")
        root.geometry("700x550")
        root.configure(bg="#0f172a")

        session = WritingSession(timeout_seconds=timeout, goal_seconds=goal_seconds)

        # Header
        lbl_title = tk.Label(root, text="✍️ Don't Stop Writing", font=("Helvetica", 20, "bold"), fg="#38bdf8", bg="#0f172a")
        lbl_title.pack(pady=(20, 5))

        lbl_timer = tk.Label(root, text=f"Time without typing: 0.0s (Limit: {timeout}s)", font=("Helvetica", 12), fg="#94a3b8", bg="#0f172a")
        lbl_timer.pack(pady=(0, 15))

        # Text Area
        txt = tk.Text(root, wrap="word", font=("Georgia", 14), bg="#1e293b", fg="#f8fafc", insertbackground="#ffffff", relief="flat", padx=16, pady=16)
        txt.pack(expand=True, fill="both", padx=25, pady=(0, 20))
        txt.focus_set()

        def on_key(event):
            session.on_keystroke(txt.get("1.0", tk.END).strip())

        txt.bind("<KeyRelease>", on_key)

        def update_loop():
            active, remaining, msg = session.check_status()
            if not active:
                if session.is_vanished:
                    txt.delete("1.0", tk.END)
                    lbl_timer.config(text="💥 POOF! You stopped typing. Text vanished!", fg="#ef4444")
                    messagebox.showwarning("Text Vanished", "You stopped typing for 5 seconds. All text has been deleted!")
                elif session.is_completed:
                    lbl_timer.config(text="🎉 CONGRATULATIONS! Goal reached!", fg="#10b981")
                    saved_path = session.save_work()
                    messagebox.showinfo("Success", f"Goal accomplished! Your draft has been saved to:\n{saved_path}")
                return

            # Visual urgency: change timer color
            if remaining < 2.0:
                color = "#ef4444"
                txt.config(fg="#64748b")  # Faded text
            elif remaining < 3.5:
                color = "#f59e0b"
                txt.config(fg="#cbd5e1")
            else:
                color = "#10b981"
                txt.config(fg="#f8fafc")

            lbl_timer.config(text=f"Time remaining before vanish: {remaining:.1f}s", fg=color)
            root.after(100, update_loop)

        root.after(100, update_loop)
        root.mainloop()
    except Exception as e:
        print(f"Tkinter GUI could not open in headless environment: {e}")
