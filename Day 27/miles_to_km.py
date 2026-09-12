import tkinter as tk
from tkinter import messagebox


def calculate_km(miles_entry: tk.Entry, result_label: tk.Label):
    """Calculates kilometers from miles entered with validation."""
    try:
        user_val = miles_entry.get().strip()
        if not user_val:
            result_label.config(text="0")
            return
        miles = float(user_val)
        km = round(miles * 1.60934, 2)
        result_label.config(text=f"{km:.2f}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid numeric value for miles.")


def start_miles_to_km_app():
    """Launches the Miles to Kilometers desktop converter GUI."""
    window = tk.Tk()
    window.title("Miles to Km Converter 🚗💨")
    window.config(padx=30, pady=30, bg="#1e1e2e")
    window.resizable(False, False)

    font_main = ("Arial", 12, "bold")
    font_result = ("Arial", 14, "bold")
    fg_color = "#cdd6f4"
    bg_color = "#1e1e2e"

    # 1. Miles Input Entry (column 1, row 0)
    miles_input = tk.Entry(
        window,
        width=10,
        font=font_main,
        bg="#313244",
        fg="#ffffff",
        insertbackground="#ffffff",
        justify="center"
    )
    miles_input.grid(column=1, row=0, padx=10, pady=10)
    miles_input.focus()

    # 2. "Miles" Label (column 2, row 0)
    miles_label = tk.Label(window, text="Miles", font=font_main, fg=fg_color, bg=bg_color)
    miles_label.grid(column=2, row=0, padx=10, pady=10)

    # 3. "is equal to" Label (column 0, row 1)
    is_equal_label = tk.Label(window, text="is equal to", font=font_main, fg=fg_color, bg=bg_color)
    is_equal_label.grid(column=0, row=1, padx=10, pady=10)

    # 4. Result value Label (column 1, row 1)
    result_label = tk.Label(window, text="0", font=font_result, fg="#a6e3a1", bg=bg_color)
    result_label.grid(column=1, row=1, padx=10, pady=10)

    # 5. "Km" Label (column 2, row 1)
    km_label = tk.Label(window, text="Km", font=font_main, fg=fg_color, bg=bg_color)
    km_label.grid(column=2, row=1, padx=10, pady=10)

    # 6. Calculate Button (column 1, row 2)
    calculate_button = tk.Button(
        window,
        text="Calculate",
        font=font_main,
        bg="#89b4fa",
        fg="#11111b",
        activebackground="#b4befe",
        cursor="hand2",
        command=lambda: calculate_km(miles_input, result_label)
    )
    calculate_button.grid(column=1, row=2, padx=10, pady=15)

    # Pressing Enter triggers calculate
    window.bind("<Return>", lambda _: calculate_km(miles_input, result_label))

    window.mainloop()


if __name__ == "__main__":
    start_miles_to_km_app()
