import tkinter as tk
from tkinter import ttk, messagebox


class MultiUnitConverterApp:
    """Advanced Multi-Unit Desktop Converter built using Tkinter and ttk widgets."""

    CONVERSION_MODES = {
        "Miles to Kilometers": ("Miles", "Km", lambda val: val * 1.60934),
        "Kilometers to Miles": ("Km", "Miles", lambda val: val / 1.60934),
        "Celsius to Fahrenheit": ("°C", "°F", lambda val: (val * 9/5) + 32),
        "Fahrenheit to Celsius": ("°F", "°C", lambda val: (val - 32) * 5/9),
        "Pounds to Kilograms": ("lbs", "kg", lambda val: val * 0.453592),
        "Kilograms to Pounds": ("kg", "lbs", lambda val: val / 0.453592),
    }

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("OmniConverter Pro - Multi-Unit Desktop App 🔄")
        self.window.config(padx=35, pady=35, bg="#1e1e2e")
        self.window.resizable(False, False)

        self.font_title = ("Arial", 14, "bold")
        self.font_main = ("Arial", 11, "bold")
        self.font_result = ("Arial", 16, "bold")

        self.setup_ui()

    def setup_ui(self):
        # Header Title
        title_label = tk.Label(
            self.window,
            text="OmniConverter Pro",
            font=self.font_title,
            fg="#89b4fa",
            bg="#1e1e2e"
        )
        title_label.grid(column=0, row=0, columnspan=3, pady=(0, 20))

        # Mode Selection Combobox
        self.mode_var = tk.StringVar(value="Miles to Kilometers")
        self.mode_dropdown = ttk.Combobox(
            self.window,
            textvariable=self.mode_var,
            values=list(self.CONVERSION_MODES.keys()),
            state="readonly",
            font=self.font_main,
            width=24
        )
        self.mode_dropdown.grid(column=0, row=1, columnspan=3, padx=10, pady=10)
        self.mode_dropdown.bind("<<ComboboxSelected>>", self.on_mode_change)

        # Input Entry
        self.entry_input = tk.Entry(
            self.window,
            width=12,
            font=self.font_main,
            bg="#313244",
            fg="#ffffff",
            insertbackground="#ffffff",
            justify="center"
        )
        self.entry_input.grid(column=1, row=2, padx=10, pady=10)
        self.entry_input.focus()

        # From Unit Label
        self.from_label = tk.Label(self.window, text="Miles", font=self.font_main, fg="#cdd6f4", bg="#1e1e2e")
        self.from_label.grid(column=2, row=2, padx=5, pady=10, sticky="w")

        # Equal to label
        eq_label = tk.Label(self.window, text="is equal to", font=self.font_main, fg="#a6adc8", bg="#1e1e2e")
        eq_label.grid(column=0, row=3, padx=10, pady=10, sticky="e")

        # Result Display Label
        self.result_label = tk.Label(self.window, text="0.00", font=self.font_result, fg="#a6e3a1", bg="#1e1e2e")
        self.result_label.grid(column=1, row=3, padx=10, pady=10)

        # To Unit Label
        self.to_label = tk.Label(self.window, text="Km", font=self.font_main, fg="#cdd6f4", bg="#1e1e2e")
        self.to_label.grid(column=2, row=3, padx=5, pady=10, sticky="w")

        # Convert Button
        convert_btn = tk.Button(
            self.window,
            text="Convert",
            font=self.font_main,
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            cursor="hand2",
            padx=15,
            pady=5,
            command=self.perform_conversion
        )
        convert_btn.grid(column=1, row=4, pady=20)

        self.window.bind("<Return>", lambda _: self.perform_conversion())

    def on_mode_change(self, _event=None):
        mode = self.mode_var.get()
        from_unit, to_unit, _ = self.CONVERSION_MODES[mode]
        self.from_label.config(text=from_unit)
        self.to_label.config(text=to_unit)
        self.perform_conversion()

    def perform_conversion(self):
        val_str = self.entry_input.get().strip()
        if not val_str:
            self.result_label.config(text="0.00")
            return

        try:
            val = float(val_str)
            mode = self.mode_var.get()
            _, _, func = self.CONVERSION_MODES[mode]
            converted = func(val)
            self.result_label.config(text=f"{converted:.2f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value.")

    def run(self):
        self.window.mainloop()


def start_multi_converter():
    app = MultiUnitConverterApp()
    app.run()


if __name__ == "__main__":
    start_multi_converter()
