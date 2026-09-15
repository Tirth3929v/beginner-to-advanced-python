import os
import sys
import tkinter as tk
from tkinter import messagebox
from password_generator import generate_secure_password

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------------------------- CONSTANTS & PALETTE ------------------------------- #
BG_DARK = "#1e1e2e"
SURFACE = "#313244"
TEXT_COLOR = "#cdd6f4"
ACCENT_BLUE = "#89b4fa"
ACCENT_GREEN = "#a6e3a1"
ACCENT_RED = "#f38ba8"
FONT_LABEL = ("Arial", 10, "bold")
FONT_INPUT = ("Arial", 11)
DEFAULT_EMAIL = "tirthpatel82032@gmail.com"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.txt")


class PasswordManagerApp:
    """Tkinter Desktop Password Manager Application."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MyPass - Password Manager 🔐")
        self.window.config(padx=40, pady=35, bg=BG_DARK)
        self.window.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # 1. Canvas with Vector Padlock Art
        self.canvas = tk.Canvas(self.window, width=200, height=200, bg=BG_DARK, highlightthickness=0)
        
        # Padlock Shackle (Silver-blue curved arch)
        self.canvas.create_arc(55, 25, 145, 135, start=0, extent=180, outline=ACCENT_BLUE, width=14, style="arc")
        
        # Padlock Body (Rounded Gold/Bronze rectangle)
        self.canvas.create_rectangle(45, 85, 155, 180, fill="#f9e2af", outline="#fab387", width=3)
        
        # Keyhole (Dark circular top with tapering slot)
        self.canvas.create_oval(92, 110, 108, 126, fill=BG_DARK, outline="")
        self.canvas.create_polygon(95, 122, 105, 122, 103, 145, 97, 145, fill=BG_DARK, outline="")

        self.canvas.grid(column=1, row=0, pady=(0, 20))

        # 2. Website Label & Entry
        website_label = tk.Label(self.window, text="Website:", font=FONT_LABEL, fg=TEXT_COLOR, bg=BG_DARK)
        website_label.grid(column=0, row=1, sticky="e", padx=(0, 10), pady=6)

        self.website_entry = tk.Entry(
            self.window,
            width=36,
            font=FONT_INPUT,
            bg=SURFACE,
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.website_entry.grid(column=1, row=1, columnspan=2, sticky="w", pady=6)
        self.website_entry.focus()

        # 3. Email/Username Label & Entry
        email_label = tk.Label(self.window, text="Email/Username:", font=FONT_LABEL, fg=TEXT_COLOR, bg=BG_DARK)
        email_label.grid(column=0, row=2, sticky="e", padx=(0, 10), pady=6)

        self.email_entry = tk.Entry(
            self.window,
            width=36,
            font=FONT_INPUT,
            bg=SURFACE,
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.email_entry.grid(column=1, row=2, columnspan=2, sticky="w", pady=6)
        self.email_entry.insert(0, DEFAULT_EMAIL)

        # 4. Password Label & Entry
        password_label = tk.Label(self.window, text="Password:", font=FONT_LABEL, fg=TEXT_COLOR, bg=BG_DARK)
        password_label.grid(column=0, row=3, sticky="e", padx=(0, 10), pady=6)

        self.password_entry = tk.Entry(
            self.window,
            width=21,
            font=FONT_INPUT,
            bg=SURFACE,
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.password_entry.grid(column=1, row=3, sticky="w", pady=6)

        # 5. Generate Password Button
        generate_btn = tk.Button(
            self.window,
            text="Generate Pass",
            font=("Arial", 9, "bold"),
            bg=ACCENT_BLUE,
            fg="#11111b",
            activebackground="#b4befe",
            cursor="hand2",
            padx=4,
            pady=2,
            command=self.on_generate_password
        )
        generate_btn.grid(column=2, row=3, sticky="w", padx=(5, 0), pady=6)

        # 6. Add Button
        add_btn = tk.Button(
            self.window,
            text="Add Password Entry",
            font=FONT_LABEL,
            bg=ACCENT_GREEN,
            fg="#11111b",
            activebackground="#94e2d5",
            cursor="hand2",
            width=33,
            pady=5,
            command=self.save_password
        )
        add_btn.grid(column=1, row=4, columnspan=2, sticky="w", pady=(15, 5))

        # Enter key triggers save
        self.window.bind("<Return>", lambda _: self.save_password())

    def on_generate_password(self):
        """Generates a secure password, populates field, and copies to clipboard."""
        self.password_entry.delete(0, tk.END)
        new_password = generate_secure_password()
        self.password_entry.insert(0, new_password)

        # Copy to clipboard
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(new_password)
        except Exception:
            pass

    def save_password(self):
        """Validates inputs, prompts confirmation, appends to data.txt, and resets input fields."""
        website = self.website_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validation: Check for empty fields
        if not website or not password:
            messagebox.showwarning(
                title="Oops! Empty Fields",
                message="Please make sure you haven't left the Website or Password fields empty!"
            )
            return

        # Confirmation Dialog
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"Please confirm the details to save:\n\n"
                    f"🌐 Website: {website}\n"
                    f"📧 Email: {email}\n"
                    f"🔑 Password: {password}\n\n"
                    f"Is it ok to save?"
        )

        if is_ok:
            # Append entry to data.txt
            with open(DATA_FILE, "a", encoding="utf-8") as file:
                file.write(f"{website} | {email} | {password}\n")

            self.website_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.website_entry.focus()
            messagebox.showinfo(title="Success", message="Credentials successfully saved to vault!")

    def run(self):
        self.window.mainloop()


def start_password_manager():
    app = PasswordManagerApp()
    app.run()


if __name__ == "__main__":
    start_password_manager()
