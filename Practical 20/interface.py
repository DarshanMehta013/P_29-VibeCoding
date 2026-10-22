
"""A simple Tkinter form for entering student information."""

import tkinter as tk
from tkinter import messagebox


def submit_information():
    """Validate required fields and display student information."""
    student_name = name_entry.get().strip()
    roll_number = roll_entry.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()

    # Check that all required fields contain information.
    if not all([student_name, roll_number, course, email]):
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields before submitting."
        )
        return

    # Display the entered details in a message box.
    messagebox.showinfo(
        "Student Information",
        f"Student Name: {student_name}\n"
        f"Roll Number: {roll_number}\n"
        f"Course: {course}\n"
        f"Email Address: {email}"
    )


def clear_fields():
    """Remove all text from the input fields."""
    for entry in (name_entry, roll_entry, course_entry, email_entry):
        entry.delete(0, tk.END)

    name_entry.focus_set()


# Create and configure the main application window.
window = tk.Tk()
window.title("Student Information Form")
window.geometry("500x400")
window.resizable(False, False)

# Keep the form centered with suitable spacing.
form = tk.Frame(window, padx=35, pady=22)
form.pack(fill="both", expand=True)

# Add the form heading.
heading = tk.Label(
    form,
    text="Student Information Form",
    font=("Arial", 18, "bold")
)
heading.grid(row=0, column=0, columnspan=2, pady=(0, 24))

# Create labels and corresponding input fields.
fields = [
    ("Student Name:", 1),
    ("Roll Number:", 2),
    ("Course:", 3),
    ("Email Address:", 4)
]

entries = []

for label_text, row in fields:
    label = tk.Label(
        form,
        text=label_text,
        font=("Arial", 11)
    )
    label.grid(row=row, column=0, padx=(0, 14), pady=8, sticky="e")

    entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=28
    )
    entry.grid(row=row, column=1, pady=8, sticky="w")
    entries.append(entry)

# Give the fields descriptive names for the button functions.
name_entry, roll_entry, course_entry, email_entry = entries

# Add the Submit, Clear, and Exit buttons.
button_frame = tk.Frame(form)
button_frame.grid(row=5, column=0, columnspan=2, pady=(24, 0))

tk.Button(
    button_frame,
    text="Submit",
    width=10,
    command=submit_information
).pack(side="left", padx=8)

tk.Button(
    button_frame,
    text="Clear",
    width=10,
    command=clear_fields
).pack(side="left", padx=8)

tk.Button(
    button_frame,
    text="Exit",
    width=10,
    command=window.destroy
).pack(side="left", padx=8)

# Place the cursor in the first field when the window opens.
name_entry.focus_set()

# Start Tkinter's event loop.
window.mainloop()
