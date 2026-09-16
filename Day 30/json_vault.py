"""
Day 30 - Resilient JSON Vault & Database Engine
Demonstrates robust error handling with json.dump, json.load, json.update,
and handling FileNotFoundError, JSONDecodeError, and KeyError.
"""

import json
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VAULT_FILE = os.path.join(os.path.dirname(__file__), "vault_data.json")

# Modern Dark Catppuccin Theme Palette
BG_DARK = "#1e1e2e"
SURFACE = "#313244"
TEXT_COLOR = "#cdd6f4"
ACCENT_BLUE = "#89b4fa"
ACCENT_GREEN = "#a6e3a1"
ACCENT_PURPLE = "#cba6f7"
ACCENT_RED = "#f38ba8"
FONT_LABEL = ("Arial", 10, "bold")
FONT_INPUT = ("Arial", 10)


# ==============================================================================
# 1. CORE JSON STORAGE ENGINE (WITH EXCEPTION HANDLING)
# ==============================================================================

def load_vault() -> dict:
    """
    Safely loads JSON vault data with full exception recovery:
    - Catches FileNotFoundError -> initializes empty dictionary
    - Catches json.JSONDecodeError -> handles empty or corrupted JSON file
    """
    try:
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        # File doesn't exist yet; return empty dictionary to start
        return {}
    except json.JSONDecodeError:
        # File exists but is corrupt or completely empty
        return {}


def save_vault_entry(website: str, email: str, password: str, notes: str = "") -> bool:
    """
    Saves or updates a credential record in JSON:
    1. Reads existing data using load_vault()
    2. Updates with new entry
    3. Writes back cleanly with indent=4
    """
    if not website or not password:
        raise ValueError("Website and Password cannot be blank.")

    data = load_vault()
    data[website] = {
        "email": email,
        "password": password,
        "notes": notes
    }

    try:
        with open(VAULT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except (IOError, OSError) as write_err:
        raise RuntimeError(f"Failed to write to vault storage: {write_err}")


def search_vault(website_query: str) -> dict:
    """
    Searches the JSON vault for a given website (case-insensitive).
    Raises KeyError if not found.
    Raises FileNotFoundError if vault file does not exist.
    """
    if not os.path.exists(VAULT_FILE):
        raise FileNotFoundError(f"Vault data file '{os.path.basename(VAULT_FILE)}' has not been created yet.")

    data = load_vault()
    query_lower = website_query.strip().lower()

    for site_key, creds in data.items():
        if site_key.lower() == query_lower:
            return {
                "website": site_key,
                "email": creds.get("email", ""),
                "password": creds.get("password", ""),
                "notes": creds.get("notes", "")
            }

    raise KeyError(f"No credentials found in vault for '{website_query}'.")


def delete_vault_entry(website_query: str) -> bool:
    """Deletes an entry from JSON storage. Raises KeyError if not present."""
    data = load_vault()
    matched_key = None
    for k in data.keys():
        if k.lower() == website_query.strip().lower():
            matched_key = k
            break

    if not matched_key:
        raise KeyError(f"Entry '{website_query}' not found.")

    del data[matched_key]
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return True


# ==============================================================================
# 2. TKINTER DESKTOP GUI INTERFACE
# ==============================================================================

class JSONVaultGUI:
    """Desktop GUI interface for Day 30 Resilient JSON Vault."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Day 30 - Resilient JSON Vault 🛡️📂")
        self.window.geometry("560x520")
        self.window.config(padx=30, pady=25, bg=BG_DARK)

        # Vector Banner Canvas
        self.canvas = tk.Canvas(self.window, width=500, height=100, bg=BG_DARK, highlightthickness=0)
        # Draw stylized document & shield
        self.canvas.create_rectangle(190, 15, 290, 85, fill=SURFACE, outline=ACCENT_BLUE, width=2)
        self.canvas.create_line(205, 30, 275, 30, fill=TEXT_COLOR, width=2)
        self.canvas.create_line(205, 45, 275, 45, fill=ACCENT_PURPLE, width=2)
        self.canvas.create_line(205, 60, 255, 60, fill=ACCENT_GREEN, width=2)
        self.canvas.create_text(240, 75, text="{ JSON }", font=("Courier", 9, "bold"), fill=ACCENT_BLUE)
        self.canvas.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # 1. Website
        tk.Label(self.window, text="Website:", font=FONT_LABEL, fg=TEXT_COLOR, bg=BG_DARK).grid(
            row=1, column=0, sticky="e", padx=(0, 10), pady=6
        )
        self.site_entry = tk.Entry(self.window, width=24, font=FONT_INPUT, bg=SURFACE, fg="#ffffff", insertbackground="#fff")
        self.site_entry.grid(row=1, column=1, sticky="w", pady=6)
        self.site_entry.focus()

        search_btn = tk.Button(
            self.window, text="🔍 Search JSON", font=("Arial", 9, "bold"),
            bg=ACCENT_BLUE, fg="#11111b", cursor="hand2", command=self.on_search
        )
        search_btn.grid(row=1, column=2, sticky="w", padx=(5, 0), pady=6)

        # 2. Email/Username
        tk.Label(self.window, text="Email/Username:", font=FONT_LABEL, fg=TEXT_COLOR, bg=BG_DARK).grid(
            row=2, column=0, sticky="e", padx=(0, 10), pady=6
        )
        self.email_entry = tk.Entry(self.window, width=37, font=FONT_INPUT, bg=SURFACE, fg="#ffffff", insertbackground="#fff")
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=6)
        self.email_entry.insert(0, "tirthpatel82032@gmail.com")

        # 3. Password
        tk.Label(self.window, text="Password:", font=FONT_LABEL, fg=TEXT_COLOR, bg=BG_DARK).grid(
            row=3, column=0, sticky="e", padx=(0, 10), pady=6
        )
        self.password_entry = tk.Entry(self.window, width=37, font=FONT_INPUT, bg=SURFACE, fg="#ffffff", insertbackground="#fff")
        self.password_entry.grid(row=3, column=1, columnspan=2, sticky="w", pady=6)

        # 4. Save Entry Button
        save_btn = tk.Button(
            self.window, text="💾 Save to JSON Vault", font=FONT_LABEL,
            bg=ACCENT_GREEN, fg="#11111b", width=34, pady=5, cursor="hand2", command=self.on_save
        )
        save_btn.grid(row=4, column=1, columnspan=2, sticky="w", pady=(15, 6))

        # 5. View Vault Explorer
        view_btn = tk.Button(
            self.window, text="👁️ Browse Full JSON Vault", font=FONT_LABEL,
            bg=ACCENT_PURPLE, fg="#11111b", width=34, pady=5, cursor="hand2", command=self.on_browse
        )
        view_btn.grid(row=5, column=1, columnspan=2, sticky="w", pady=6)

        # Status Bar Label
        self.status_lbl = tk.Label(
            self.window, text="Ready. Protected by Python Exception Handling.",
            font=("Arial", 8, "italic"), fg="#a6adc8", bg=BG_DARK
        )
        self.status_lbl.grid(row=6, column=0, columnspan=3, pady=(15, 0))

    def on_search(self):
        query = self.site_entry.get().strip()
        if not query:
            messagebox.showwarning(title="Empty Search", message="Please type a Website name to search!")
            return

        try:
            entry = search_vault(query)
        except FileNotFoundError as fnf_err:
            messagebox.showerror(title="File Not Found", message=f"❌ {fnf_err}\nAdd an entry first to initialize vault.")
            self.status_lbl.config(text="FileNotFoundError handled cleanly.", fg=ACCENT_RED)
        except KeyError as key_err:
            messagebox.showinfo(title="Not Found", message=f"⚠️ {key_err}")
            self.status_lbl.config(text=f"KeyError handled: '{query}' not found.", fg=ACCENT_BLUE)
        else:
            # Reached only if NO exceptions occurred!
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, entry["email"])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, entry["password"])

            try:
                self.window.clipboard_clear()
                self.window.clipboard_append(entry["password"])
            except Exception:
                pass

            messagebox.showinfo(
                title=f"Credentials: {entry['website']}",
                message=f"🌐 Website: {entry['website']}\n"
                        f"📧 Email: {entry['email']}\n"
                        f"🔑 Password: {entry['password']}\n\n"
                        f"✨ (Password copied to clipboard!)"
            )
            self.status_lbl.config(text=f"Loaded credentials for '{entry['website']}'.", fg=ACCENT_GREEN)

    def on_save(self):
        website = self.site_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        try:
            save_vault_entry(website, email, password)
        except ValueError as val_err:
            messagebox.showwarning(title="Validation Error", message=str(val_err))
            self.status_lbl.config(text="Validation error prevented invalid save.", fg=ACCENT_RED)
        except RuntimeError as run_err:
            messagebox.showerror(title="I/O Error", message=str(run_err))
        else:
            self.site_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.site_entry.focus()
            messagebox.showinfo(title="Success", message=f"Entry for '{website}' committed to {os.path.basename(VAULT_FILE)}!")
            self.status_lbl.config(text=f"Committed '{website}' to JSON vault.", fg=ACCENT_GREEN)

    def on_browse(self):
        data = load_vault()
        if not data:
            messagebox.showinfo(title="Vault Empty", message="JSON Vault is currently empty! Add entries to begin.")
            return

        browser_win = tk.Toplevel(self.window)
        browser_win.title("JSON Vault Browser 🗄️")
        browser_win.geometry("640x380")
        browser_win.config(bg=BG_DARK, padx=20, pady=20)

        tk.Label(
            browser_win, text=f"Total Records: {len(data)}",
            font=("Arial", 11, "bold"), fg=ACCENT_BLUE, bg=BG_DARK
        ).pack(pady=(0, 10))

        cols = ("Website", "Email / Username", "Password")
        tree = ttk.Treeview(browser_win, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=190)

        for site, info in data.items():
            tree.insert("", tk.END, values=(site, info.get("email", ""), info.get("password", "")))

        tree.pack(fill=tk.BOTH, expand=True)

        def copy_sel():
            sel = tree.selection()
            if sel:
                item = tree.item(sel[0])
                pwd = item["values"][2]
                try:
                    self.window.clipboard_clear()
                    self.window.clipboard_append(pwd)
                    messagebox.showinfo("Copied", "Password copied to clipboard!", parent=browser_win)
                except Exception:
                    pass

        tk.Button(
            browser_win, text="📋 Copy Selected Password", font=FONT_LABEL,
            bg=ACCENT_GREEN, fg="#11111b", cursor="hand2", command=copy_sel
        ).pack(pady=(12, 0))

    def run(self):
        self.window.mainloop()


# ==============================================================================
# 3. TERMINAL CLI EXPLORER
# ==============================================================================

def run_terminal_vault_explorer():
    """Terminal CLI for testing JSON CRUD operations and seeing exception flow in real-time."""
    print("\n" + "=" * 65)
    print(" 📂 TERMINAL JSON VAULT EXPLORER (EXCEPTION HANDLING LAB)")
    print("=" * 65)

    while True:
        try:
            print("Actions: [1] Search, [2] Add/Update, [3] List All, [4] Delete, [5] Return")
            cmd = input("👉 Enter choice (1-5): ").strip()

            if cmd == "1":
                query = input(" Website to search: ").strip()
                try:
                    res = search_vault(query)
                    print(f" ✅ Found: {res['website']} | {res['email']} | {res['password']}")
                except FileNotFoundError as err:
                    print(f" ❌ FileNotFoundError: {err}")
                except KeyError as err:
                    print(f" ❌ KeyError: {err}")

            elif cmd == "2":
                site = input(" Website: ").strip()
                email = input(" Email/Username: ").strip()
                pwd = input(" Password: ").strip()
                try:
                    save_vault_entry(site, email, pwd)
                    print(f" ✅ Saved entry for '{site}' to JSON vault!")
                except ValueError as val_err:
                    print(f" ❌ ValueError: {val_err}")

            elif cmd == "3":
                data = load_vault()
                if not data:
                    print(" ℹ️ Vault is empty or file not found yet.")
                else:
                    print(f"\n --- Vault Records ({len(data)}) ---")
                    for s, info in data.items():
                        print(f" • {s:20s} -> {info.get('email', ''):25s} | {info.get('password', '')}")
                    print(" -------------------------------")

            elif cmd == "4":
                del_site = input(" Website to delete: ").strip()
                try:
                    delete_vault_entry(del_site)
                    print(f" ✅ Successfully removed '{del_site}' from JSON vault.")
                except KeyError as k_err:
                    print(f" ❌ KeyError: {k_err}")

            elif cmd == "5" or cmd.lower() in ("exit", "q", "quit"):
                print("👋 Returning to main menu...\n")
                break
            else:
                print("⚠️ Invalid choice!")
            print()

        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Exiting CLI vault...\n")
            break


def launch_gui_vault():
    app = JSONVaultGUI()
    app.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    launch_gui_vault()
