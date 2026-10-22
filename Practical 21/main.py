
import tkinter as tk
from tkinter import messagebox

# This function runs when the Submit button is clicked.
def submit_name():
    name = name_entry.get().strip()

    # Check whether the user entered a name.
    if name:
        messagebox.showinfo(
            "Greeting",
            f"Hello, {name}! Welcome to my GUI application."
        )
    else:
        messagebox.showwarning(
            "Name Required",
            "Please enter your name first."
        )

# Create the main application window.
window = tk.Tk()
window.title("My First GUI Application")
window.geometry("400x220")

# Add a welcome message.
welcome_label = tk.Label(
    window,
    text="Welcome! Please enter your name:",
    font=("Arial", 14)
)
welcome_label.pack(pady=20)

# Add a text field for entering the name.
name_entry = tk.Entry(window, font=("Arial", 12), width=30)
name_entry.pack()
name_entry.focus()

# Add a button that calls submit_name when clicked.
submit_button = tk.Button(
    window,
    text="Submit",
    command=submit_name
)
submit_button.pack(pady=15)

# Keep the window open.
window.mainloop()
