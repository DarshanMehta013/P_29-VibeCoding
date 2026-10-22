
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

# Connect to the database in the current practical folder.
connection = sqlite3.connect("student_records.db")
cursor = connection.cursor()

# Create the student registration table if it does not exist.
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    roll_number TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    course TEXT NOT NULL
)
""")
connection.commit()

def clear_form():
    """Clear all registration fields."""
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    records_table.selection_remove(records_table.selection())

def view_records():
    """Display all records stored in SQLite."""
    for item in records_table.get_children():
        records_table.delete(item)

    cursor.execute("""
        SELECT id, full_name, roll_number, email, phone, course
        FROM student_records ORDER BY id
    """)

    for record in cursor.fetchall():
        records_table.insert("", tk.END, values=record)

def submit_record():
    """Validate and insert a new student record."""
    full_name = name_entry.get().strip()
    roll_number = roll_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    course = course_entry.get().strip()

    if not all([full_name, roll_number, email, phone, course]):
        messagebox.showwarning("Missing Details", "Please fill in all fields.")
        return

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
        return

    if not phone.isdigit() or len(phone) != 10:
        messagebox.showwarning("Invalid Phone", "Enter a 10-digit phone number.")
        return

    try:
        cursor.execute("""
            INSERT INTO student_records
                (full_name, roll_number, email, phone, course)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, roll_number, email, phone, course))

        connection.commit()
        view_records()
        clear_form()
        messagebox.showinfo("Success", "Student record saved successfully.")

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Duplicate Roll Number",
            "This roll number already exists."
        )
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))

def delete_selected():
    """Delete the selected student record."""
    selected = records_table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a record from the table first."
        )
        return

    record = records_table.item(selected[0], "values")
    student_id = record[0]

    if not messagebox.askyesno(
        "Confirm Delete",
        f"Delete the record for {record[1]}?"
    ):
        return

    try:
        cursor.execute(
            "DELETE FROM student_records WHERE id = ?",
            (student_id,)
        )
        connection.commit()
        view_records()
        clear_form()
        messagebox.showinfo("Success", "Student record deleted successfully.")

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))

def close_app():
    """Close the database connection safely."""
    connection.close()
    window.destroy()

# Create the main application window.
window = tk.Tk()
window.title("Student Registration Form")
window.geometry("1050x600")
window.protocol("WM_DELETE_WINDOW", close_app)

# Registration form.
form = ttk.LabelFrame(window, text="Enter Student Details", padding=12)
form.pack(fill="x", padx=12, pady=12)

ttk.Label(form, text="Full Name:").grid(row=0, column=0, padx=6, pady=8, sticky="w")
name_entry = ttk.Entry(form, width=28)
name_entry.grid(row=0, column=1, padx=6, pady=8)

ttk.Label(form, text="Roll Number:").grid(row=0, column=2, padx=6, pady=8, sticky="w")
roll_entry = ttk.Entry(form, width=28)
roll_entry.grid(row=0, column=3, padx=6, pady=8)

ttk.Label(form, text="Email:").grid(row=1, column=0, padx=6, pady=8, sticky="w")
email_entry = ttk.Entry(form, width=28)
email_entry.grid(row=1, column=1, padx=6, pady=8)

ttk.Label(form, text="Phone:").grid(row=1, column=2, padx=6, pady=8, sticky="w")
phone_entry = ttk.Entry(form, width=28)
phone_entry.grid(row=1, column=3, padx=6, pady=8)

ttk.Label(form, text="Course:").grid(row=2, column=0, padx=6, pady=8, sticky="w")
course_entry = ttk.Entry(form, width=28)
course_entry.grid(row=2, column=1, padx=6, pady=8)

# Buttons for registration and record management.
buttons = ttk.Frame(window)
buttons.pack(fill="x", padx=12, pady=5)

ttk.Button(buttons, text="Submit", command=submit_record).pack(side="left", padx=5)
ttk.Button(buttons, text="View Records", command=view_records).pack(side="left", padx=5)
ttk.Button(buttons, text="Clear Form", command=clear_form).pack(side="left", padx=5)
ttk.Button(buttons, text="Delete Selected Record", command=delete_selected).pack(side="left", padx=5)

# Table for displaying registered students.
table_frame = ttk.Frame(window)
table_frame.pack(fill="both", expand=True, padx=12, pady=12)

columns = ("id", "full_name", "roll_number", "email", "phone", "course")
records_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

headings = ["ID", "Full Name", "Roll Number", "Email", "Phone", "Course"]

for column, heading in zip(columns, headings):
    records_table.heading(column, text=heading)
    records_table.column(column, width=155, anchor="center")

records_table.pack(side="left", fill="both", expand=True)

# Add a vertical scrollbar to the records table.
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=records_table.yview
)
scrollbar.pack(side="right", fill="y")
records_table.configure(yscrollcommand=scrollbar.set)

# Load saved records when the application starts.
view_records()

window.mainloop()
