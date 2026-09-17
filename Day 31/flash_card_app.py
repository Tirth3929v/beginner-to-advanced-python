"""
Day 31 - Flash Card Language Learning Desktop Application Capstone
Built with Tkinter Canvas, dynamic card flip timers (after()),
CSV data persistence, and active learning state tracking.
"""

import csv
import os
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Color Palette
BACKGROUND_COLOR = "#B1DDC6"
CARD_FRONT_BG = "#FFFFFF"
CARD_BACK_BG = "#91C2AF"
TEXT_DARK = "#1E1E2E"
TEXT_MUTED = "#6C7086"
TEXT_LIGHT = "#FFFFFF"
ACCENT_GREEN = "#A6E3A1"
ACCENT_RED = "#F38BA8"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ORIGINAL_DATA_FILE = os.path.join(DATA_DIR, "french_words.csv")
WORDS_TO_LEARN_FILE = os.path.join(DATA_DIR, "words_to_learn.csv")


class FlashCardApp:
    """Complete Flash Card learning engine with automated 3-second flip timer."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Flashy - Language Learning Flash Card Studio 📇🇫🇷")
        self.window.config(padx=40, pady=30, bg=BACKGROUND_COLOR)
        self.window.resizable(False, False)

        self.current_card = {}
        self.to_learn = self.load_word_data()
        self.flip_timer = None

        # ----------------- UI SETUP -----------------
        # 1. Main Canvas Card
        self.canvas = tk.Canvas(self.window, width=700, height=420, bg=BACKGROUND_COLOR, highlightthickness=0)
        # Vector Rounded Card Shape
        self.card_bg = self.canvas.create_rectangle(15, 15, 685, 405, fill=CARD_FRONT_BG, outline="", width=0)
        self.card_title = self.canvas.create_text(350, 120, text="Language", font=("Arial", 32, "italic"), fill=TEXT_MUTED)
        self.card_word = self.canvas.create_text(350, 230, text="Word", font=("Arial", 50, "bold"), fill=TEXT_DARK)
        self.card_counter = self.canvas.create_text(350, 360, text="", font=("Arial", 14), fill=TEXT_MUTED)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # 2. Control Buttons
        # Cross / Unknown Button (Red)
        self.unknown_btn = tk.Button(
            self.window,
            text="❌ Still Learning",
            font=("Arial", 12, "bold"),
            bg="#FF6B6B",
            fg="#FFFFFF",
            activebackground="#FA5252",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.next_card
        )
        self.unknown_btn.grid(row=1, column=0, sticky="e", padx=(0, 25))

        # Check / Known Button (Green)
        self.known_btn = tk.Button(
            self.window,
            text="✅ Mastered Word",
            font=("Arial", 12, "bold"),
            bg="#51CF66",
            fg="#FFFFFF",
            activebackground="#40C057",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.is_known
        )
        self.known_btn.grid(row=1, column=1, sticky="w", padx=(25, 0))

        # Keyboard shortcuts
        self.window.bind("<Left>", lambda _: self.next_card())
        self.window.bind("<Right>", lambda _: self.is_known())
        self.window.bind("<space>", lambda _: self.flip_card())

        # Start initial card
        self.next_card()

    def load_word_data(self) -> list:
        """Loads words from words_to_learn.csv if present, else original word list."""
        os.makedirs(DATA_DIR, exist_ok=True)
        target_file = WORDS_TO_LEARN_FILE if os.path.exists(WORDS_TO_LEARN_FILE) else ORIGINAL_DATA_FILE

        words = []
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    words.append({"French": row.get("French", ""), "English": row.get("English", "")})
        except Exception:
            # Emergency fallback word list
            words = [
                {"French": "partie", "English": "part"},
                {"French": "histoire", "English": "history"},
                {"French": "chercher", "English": "search"},
                {"French": "monde", "English": "world"},
                {"French": "temps", "English": "time"},
            ]

        if not words:
            words = [{"French": "bonjour", "English": "hello"}]
        return words

    def next_card(self):
        """Picks a new random word, resets timer to flip in 3000ms."""
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)

        if not self.to_learn:
            messagebox.showinfo(
                title="Congratulations! 🏆",
                message="You have mastered all the flash cards in this deck!\nResetting deck from original words..."
            )
            if os.path.exists(WORDS_TO_LEARN_FILE):
                try:
                    os.remove(WORDS_TO_LEARN_FILE)
                except Exception:
                    pass
            self.to_learn = self.load_word_data()

        self.current_card = random.choice(self.to_learn)

        # Render Front of Card (French)
        self.canvas.itemconfig(self.card_bg, fill=CARD_FRONT_BG)
        self.canvas.itemconfig(self.card_title, text="French 🇫🇷", fill=TEXT_MUTED)
        self.canvas.itemconfig(self.card_word, text=self.current_card["French"], fill=TEXT_DARK)
        self.canvas.itemconfig(
            self.card_counter,
            text=f"📚 Cards Remaining to Learn: {len(self.to_learn)}  (Press Space to flip immediately)",
            fill=TEXT_MUTED
        )

        # Schedule automatic card flip after 3 seconds (3000 ms)
        self.flip_timer = self.window.after(3000, self.flip_card)

    def flip_card(self):
        """Flips card to show the English translation."""
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)
            self.flip_timer = None

        self.canvas.itemconfig(self.card_bg, fill=CARD_BACK_BG)
        self.canvas.itemconfig(self.card_title, text="English 🇬🇧", fill=TEXT_DARK)
        self.canvas.itemconfig(self.card_word, text=self.current_card.get("English", ""), fill=TEXT_DARK)
        self.canvas.itemconfig(
            self.card_counter,
            text=f"✅ Mark Mastered or ❌ Keep Practicing",
            fill=TEXT_DARK
        )

    def is_known(self):
        """User knows the word: remove from deck, save remaining words to CSV, and show next card."""
        if self.current_card in self.to_learn:
            self.to_learn.remove(self.current_card)

        # Save updated progress to words_to_learn.csv
        try:
            with open(WORDS_TO_LEARN_FILE, "w", newline="", encoding="utf-8") as f:
                fieldnames = ["French", "English"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in self.to_learn:
                    writer.writerow(row)
        except Exception:
            pass

        self.next_card()

    def run(self):
        self.window.mainloop()


def start_flash_card_app():
    app = FlashCardApp()
    app.run()


if __name__ == "__main__":
    start_flash_card_app()
