
"""A first Tkinter window with a personalized greeting."""

import tkinter as tk
from tkinter import messagebox


def submit_name():
    """Show a greeting or ask the user to enter a name."""
    name = name_entry.get().strip()

    if not name:
        messagebox.showwarning(
            "Name Required",
            "Please enter your name first."
        )
        return

    messagebox.showinfo(
        "Welcome",
        f"Hello, {name}! Welcome to my first GUI application."
    )


# Create and configure the main application window.
window = tk.Tk()
window.title("My First GUI Application")
window.geometry("500x350")
window.resizable(False, False)

# Add the welcome heading.
heading = tk.Label(
    window,
    text="Welcome!",
    font=("Arial", 22, "bold")
)
heading.pack(pady=(45, 25))

# Ask the user to enter their name.
prompt = tk.Label(
    window,
    text="Please enter your name:",
    font=("Arial", 12)
)
prompt.pack(pady=5)

# Create a text field for the name.
name_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=30
)
name_entry.pack(pady=10)
name_entry.focus_set()

# Clicking Submit runs the submit_name function.
submit_button = tk.Button(
    window,
    text="Submit",
    font=("Arial", 11),
    command=submit_name
)
submit_button.pack(pady=15)

# Keep the window open and respond to user actions.
window.mainloop()
