import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        self.current = ""
        self.total = 0
        self.input_value = True
        self.check_sum = False
        self.op = ""
        self.result = False

        self.create_widgets()

    def create_widgets(self):
        # Display
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(expand=True, fill="both")

        self.display = tk.Entry(
            self.display_frame,
            font=("Arial", 16),
            width=20,
            justify="right",
            state="readonly"
        )
        self.display.pack(padx=10, pady=10, ipady=10)

        # Buttons frame
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(expand=True, fill="both")

        # Button layout
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                if btn_text == '0':
                    btn = tk.Button(
                        self.buttons_frame,
                        text=btn_text,
                        font=("Arial", 14),
                        command=lambda x=btn_text: self.button_click(x)
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky="nsew", padx=2, pady=2)
                elif btn_text == '=':
                    btn = tk.Button(
                        self.buttons_frame,
                        text=btn_text,
                        font=("Arial", 14),
                        bg="#ff9500",
                        fg="white",
                        command=self.calculate
                    )
                    btn.grid(row=i, column=j+1, sticky="nsew", padx=2, pady=2)
                else:
                    btn = tk.Button(
                        self.buttons_frame,
                        text=btn_text,
                        font=("Arial", 14),
                        command=lambda x=btn_text: self.button_click(x)
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

        # Configure grid weights
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.buttons_frame.grid_columnconfigure(j, weight=1)

    def button_click(self, value):
        if value in "0123456789.":
            self.number_press(value)
        elif value in "+-×÷":
            self.operation_press(value)
        elif value == "C":
            self.clear()
        elif value == "±":
            self.sign_change()
        elif value == "%":
            self.percentage()

    def number_press(self, num):
        if self.input_value:
            self.current = ""
            self.input_value = False

        if num == "." and "." in self.current:
            return

        self.current += str(num)
        self.update_display()

    def operation_press(self, op):
        if self.current:
            if self.check_sum and self.op:
                self.calculate()
            else:
                self.total = float(self.current)

            self.current = ""
            self.check_sum = True
            self.op = op
            self.input_value = True

    def calculate(self):
        if self.op and self.current:
            try:
                if self.op == "+":
                    self.total = self.total + float(self.current)
                elif self.op == "-":
                    self.total = self.total - float(self.current)
                elif self.op == "×":
                    self.total = self.total * float(self.current)
                elif self.op == "÷":
                    if float(self.current) == 0:
                        messagebox.showerror("Error", "Cannot divide by zero!")
                        self.clear()
                        return
                    self.total = self.total / float(self.current)

                self.current = str(self.total)
                if self.current.endswith('.0'):
                    self.current = self.current[:-2]

                self.update_display()
                self.input_value = True
                self.check_sum = False
                self.op = ""

            except ValueError:
                messagebox.showerror("Error", "Invalid input!")
                self.clear()

    def clear(self):
        self.current = ""
        self.total = 0
        self.input_value = True
        self.check_sum = False
        self.op = ""
        self.update_display()

    def sign_change(self):
        if self.current:
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.update_display()

    def percentage(self):
        if self.current:
            self.current = str(float(self.current) / 100)
            self.update_display()

    def update_display(self):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current if self.current else "0")
        self.display.config(state="readonly")

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()