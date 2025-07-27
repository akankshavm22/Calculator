import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("CALCULATOR")
        self.root.geometry("300x450")
        self.root.resizable(False, False)
        
        # Custom font
        self.button_font = font.Font(size=14, weight='bold')
        self.display_font = font.Font(size=20, weight='bold')
        
        # Create display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display = tk.Entry(
            root, 
            textvariable=self.display_var, 
            font=self.display_font, 
            justify="right", 
            bd=10, 
            insertwidth=2,
            width=14,
            borderwidth=4,
            background="#f0f0f0"
        )
        self.display.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Create buttons
        self.create_buttons()
        
        # Initialize calculator state
        self.current_input = "0"
        self.operation = None
        self.previous_value = None
        self.reset_next_input = False
    
    def create_buttons(self):
        # Button layout similar to the image
        buttons = [
            ("AC", 1, 0), ("DE", 1, 1), ("%", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("+", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("00", 5, 0), ("0", 5, 1), (".", 5, 2), ("=", 5, 3)
        ]
        
        for (text, row, col) in buttons:
            # Color coding
            if text in ["AC", "DE"]:
                bg = "#ff6666"  # Light red for clear buttons
            elif text in ["="]:
                bg = "#66b3ff"  # Light blue for equals
            elif text in ["/", "+", "-", "%"]:
                bg = "#ffcc99"  # Light orange for operators
            else:
                bg = "#f0f0f0"  # Light gray for numbers
            
            button = tk.Button(
                self.root, 
                text=text,
                font=self.button_font,
                bg=bg,
                padx=20,
                pady=15,
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, sticky="nsew")
            
            # Configure row/column weights
            self.root.rowconfigure(row, weight=1)
            self.root.columnconfigure(col, weight=1)
    
    def on_button_click(self, button_text):
        if button_text == "AC":
            self.current_input = "0"
            self.operation = None
            self.previous_value = None
        elif button_text == "DE":
            if len(self.current_input) > 1:
                self.current_input = self.current_input[:-1]
            else:
                self.current_input = "0"
        elif button_text in ["+", "-", "/", "%"]:
            if self.operation is not None:
                self.calculate()
            self.operation = button_text
            self.previous_value = float(self.current_input)
            self.reset_next_input = True
        elif button_text == "=":
            self.calculate()
            self.operation = None
        elif button_text == ".":
            if "." not in self.current_input:
                self.current_input += "."
        else:  # Numbers
            if self.current_input == "0" or self.reset_next_input:
                self.current_input = button_text
                self.reset_next_input = False
            else:
                self.current_input += button_text
        
        self.display_var.set(self.current_input)
    
    def calculate(self):
        if self.operation and self.previous_value is not None:
            current_value = float(self.current_input)
            try:
                if self.operation == "+":
                    result = self.previous_value + current_value
                elif self.operation == "-":
                    result = self.previous_value - current_value
                elif self.operation == "/":
                    result = self.previous_value / current_value
                elif self.operation == "%":
                    result = self.previous_value % current_value
                
                self.current_input = str(result)
                if self.current_input.endswith(".0"):
                    self.current_input = self.current_input[:-2]
                self.previous_value = result
            except ZeroDivisionError:
                self.current_input = "Error"
                self.previous_value = None
                self.operation = None

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()