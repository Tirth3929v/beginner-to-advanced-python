import json
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
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
ACCENT_PURPLE = "#cba6f7"
ACCENT_RED = "#f38ba8"
FONT_LABEL = ("Arial", 10, "bold")
FONT_INPUT = ("Arial", 11)
DEFAULT_EMAIL = "tirthpatel82032@gmail.com"
DATA_TXT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.txt")
DATA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


class PasswordManagerApp:
    """Tkinter Desktop Password Manager Application with Search and Vault inspection."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MyPass - Password Manager 🔐")
        self.window.config(padx=40, pady=30, bg=BG_DARK)
        self.window.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # 1. Canvas with Vector Padlock Art
        self.canvas = tk.Canvas(self.window, width=200, height=180, bg=BG_DARK, highlightthickness=0)
        
        # Padlock Shackle
        self.canvas.create_arc(55, 20, 145, 125, start=0, extent=180, outline=ACCENT_BLUE, width=14, style="arc")
        
        # Padlock Body
        self.canvas.create_rectangle(45, 75, 155, 165, fill="#f9e2af", outline="#fab387", width=3)
        
        # Keyhole
        self.canvas.create_oval(92, 98, 108, 114, fill=BG_DARK, outline="")
        self.canvas.create_polygon(95, 110, 105, 110, 103, 133, 97, 133, fill=BG_DARK, outline="")

        self.canvas.grid(column=1, row=0, pady=(0, 15))

        # 2. Website Label, Entry & Search Button
        website_label = tk.Label(self.window, text="Website:", font=FONT_LABEL, fg=TEXT_COLOR, bg=BG_DARK)
        website_label.grid(column=0, row=1, sticky="e", padx=(0, 10), pady=6)

        self.website_entry = tk.Entry(
            self.window,
            width=21,
            font=FONT_INPUT,
            bg=SURFACE,
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.website_entry.grid(column=1, row=1, sticky="w", pady=6)
        self.website_entry.focus()

        search_btn = tk.Button(
            self.window,
            text="🔍 Search",
            font=("Arial", 9, "bold"),
            bg=ACCENT_BLUE,
            fg="#11111b",
            activebackground="#b4befe",
            cursor="hand2",
            width=13,
            pady=2,
            command=self.search_password
        )
        search_btn.grid(column=2, row=1, sticky="w", padx=(5, 0), pady=6)

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
            width=13,
            pady=2,
            command=self.on_generate_password
        )
        generate_btn.grid(column=2, row=3, sticky="w", padx=(5, 0), pady=6)

        # 6. Add Password Button
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
        add_btn.grid(column=1, row=4, columnspan=2, sticky="w", pady=(12, 5))

        # 7. View All Vault Passwords Button
        view_btn = tk.Button(
            self.window,
            text="👁️ View All Vault Passwords",
            font=FONT_LABEL,
            bg=ACCENT_PURPLE,
            fg="#11111b",
            activebackground="#b4befe",
            cursor="hand2",
            width=33,
            pady=5,
            command=self.view_vault
        )
        view_btn.grid(column=1, row=5, columnspan=2, sticky="w", pady=(0, 5))

        # Enter key triggers save
        self.window.bind("<Return>", lambda _: self.save_password())

    def on_generate_password(self):
        """Generates a secure password, populates field, and copies to clipboard."""
        self.password_entry.delete(0, tk.END)
        new_password = generate_secure_password()
        self.password_entry.insert(0, new_password)

        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(new_password)
        except Exception:
            pass

    def search_password(self):
        """Searches for website credentials in JSON and text storage, displaying matching password."""
        website = self.website_entry.get().strip()
        if not website:
            messagebox.showwarning(title="Search Empty", message="Please enter a Website name to search!")
            return

        found_entry = None

        # Check JSON storage first
        if os.path.exists(DATA_JSON):
            try:
                with open(DATA_JSON, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Case-insensitive lookup
                    for key, val in data.items():
                        if key.lower() == website.lower():
                            found_entry = (key, val.get("email", ""), val.get("password", ""))
                            break
            except Exception:
                pass

        # Fallback to checking data.txt
        if not found_entry and os.path.exists(DATA_TXT):
            try:
                with open(DATA_TXT, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 3 and parts[0].lower() == website.lower():
                            found_entry = (parts[0], parts[1], parts[2])
                            break
            except Exception:
                pass

        if found_entry:
            site_name, email, password = found_entry
            # Fill inputs so user can see it right away
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, email)
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

            # Copy to clipboard
            try:
                self.window.clipboard_clear()
                self.window.clipboard_append(password)
            except Exception:
                pass

            messagebox.showinfo(
                title=f"Credentials for {site_name}",
                message=f"🌐 Website: {site_name}\n"
                        f"📧 Email: {email}\n"
                        f"🔑 Password: {password}\n\n"
                        f"✨ (Password has been copied to your clipboard!)"
            )
        else:
            messagebox.showerror(
                title="Not Found",
                message=f"No saved credentials found for '{website}'.\nClick 'View All Vault Passwords' to see saved entries."
            )

    def view_vault(self):
        """Opens a popup window displaying all saved websites, usernames, and passwords in a table."""
        entries = []

        # Load from JSON
        if os.path.exists(DATA_JSON):
            try:
                with open(DATA_JSON, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for site, info in data.items():
                        entries.append((site, info.get("email", ""), info.get("password", "")))
            except Exception:
                pass

        # Load from TXT if JSON was empty
        if not entries and os.path.exists(DATA_TXT):
            try:
                with open(DATA_TXT, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 3:
                            entries.append((parts[0], parts[1], parts[2]))
            except Exception:
                pass

        if not entries:
            messagebox.showinfo(title="Vault Empty", message="Your password vault is currently empty. Add some entries first!")
            return

        # Vault Viewer Window
        vault_win = tk.Toplevel(self.window)
        vault_win.title("Password Vault Explorer 🗄️")
        vault_win.geometry("620x350")
        vault_win.config(bg=BG_DARK, padx=20, pady=20)

        header = tk.Label(
            vault_win,
            text=f"Saved Credentials Vault ({len(entries)} entries)",
            font=("Arial", 12, "bold"),
            fg=ACCENT_BLUE,
            bg=BG_DARK
        )
        header.pack(pady=(0, 10))

        # Treeview table
        columns = ("Website", "Email / Username", "Password")
        tree = ttk.Treeview(vault_win, columns=columns, show="headings", height=10)
        tree.heading("Website", text="Website")
        tree.heading("Email / Username", text="Email / Username")
        tree.heading("Password", text="Password")

        tree.column("Website", width=160)
        tree.column("Email / Username", width=220)
        tree.column("Password", width=180)

        for item in entries:
            tree.insert("", tk.END, values=item)

        tree.pack(fill=tk.BOTH, expand=True)

        def copy_selected():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                pwd = item["values"][2]
                try:
                    self.window.clipboard_clear()
                    self.window.clipboard_append(pwd)
                    messagebox.showinfo("Copied", "Password copied to clipboard!", parent=vault_win)
                except Exception:
                    pass

        copy_btn = tk.Button(
            vault_win,
            text="📋 Copy Selected Password",
            font=FONT_LABEL,
            bg=ACCENT_GREEN,
            fg="#11111b",
            cursor="hand2",
            command=copy_selected
        )
        copy_btn.pack(pady=(10, 0))

    def save_password(self):
        """Validates inputs, appends to JSON and data.txt, and resets input fields."""
        website = self.website_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not password:
            messagebox.showwarning(
                title="Oops! Empty Fields",
                message="Please make sure you haven't left the Website or Password fields empty!"
            )
            return

        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }

        # 1. Update JSON storage
        try:
            with open(DATA_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data.update(new_data)

        with open(DATA_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        # 2. Append to data.txt backup
        with open(DATA_TXT, "a", encoding="utf-8") as file:
            file.write(f"{website} | {email} | {password}\n")

        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.website_entry.focus()
        messagebox.showinfo(title="Success", message=f"Credentials for '{website}' successfully saved to vault!")


    def run(self):
        self.window.mainloop()


def start_password_manager():
    app = PasswordManagerApp()
    app.run()


if __name__ == "__main__":
    start_password_manager()
