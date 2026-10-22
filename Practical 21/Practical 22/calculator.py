import tkinter as tk
from tkinter import messagebox
import ast
import operator

# Allow only basic arithmetic operations.
OPERATIONS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def calculate_node(node):
    """Safely calculate a basic arithmetic expression."""
    if isinstance(node, ast.Expression):
        return calculate_node(node.body)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATIONS:
        left = calculate_node(node.left)
        right = calculate_node(node.right)
        return OPERATIONS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATIONS:
        return OPERATIONS[type(node.op)](calculate_node(node.operand))

    raise ValueError("Invalid calculation")

def press_button(value):
    """Handle calculator button clicks."""
    current = display_var.get()

    if value == "C":
        display_var.set("")
        return

    if value == "=":
        try:
            expression = ast.parse(current, mode="eval")
            result = calculate_node(expression)
            display_var.set(str(result))
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero.")
        except (ValueError, SyntaxError, TypeError, OverflowError):
            messagebox.showerror("Error", "Invalid calculation.")
        return

    # Start a fresh expression after an error message.
    if current == "Error":
        current = ""

    display_var.set(current + value)

# Create the calculator window.
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("320x380")
window.resizable(False, False)

display_var = tk.StringVar()

# Display area for the expression and result.
display = tk.Entry(
    window,
    textvariable=display_var,
    font=("Arial", 20),
    justify="right",
    state="normal"
)
display.grid(row=0, column=0, columnspan=4,
             padx=10, pady=15, sticky="nsew")

# Arrange the calculator buttons in a grid.
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("C", 4, 0), ("0", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

for label, row, column in buttons:
    button = tk.Button(
        window,
        text=label,
        font=("Arial", 16),
        width=5,
        height=2,
        command=lambda value=label: press_button(value)
    )
    button.grid(row=row, column=column, padx=4, pady=4)

window.mainloop()
