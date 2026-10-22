
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connect to the database and create the students table.
connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL UNIQUE,
    course TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
connection.commit()

selected_id = None

def clear_fields():
    """Clear all input fields."""
    global selected_id
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    selected_id = None
    student_table.selection_remove(student_table.selection())

def view_students():
    """Display all student records in the table."""
    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute(
        "SELECT id, name, roll_no, course, email FROM students ORDER BY id"
    )

    for row in cursor.fetchall():
        student_table.insert("", tk.END, values=row)

def add_student():
    """Insert a new student into the database."""
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()

    if not all([name, roll, course, email]):
        messagebox.showwarning("Missing Data", "Please fill in all fields.")
        return

    try:
        cursor.execute(
            "INSERT INTO students (name, roll_no, course, email) VALUES (?, ?, ?, ?)",
            (name, roll, course, email)
        )
        connection.commit()
        view_students()
        clear_fields()
        messagebox.showinfo("Success", "Student added successfully.")

    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate Roll Number", "This roll number already exists.")

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))

def select_student(event):
    """Fill the input fields when a row is selected."""
    global selected_id
    selected = student_table.selection()

    if not selected:
        return

    values = student_table.item(selected[0], "values")
    selected_id = int(values[0])

    clear_input_values = [name_entry, roll_entry, course_entry, email_entry]
    for entry, value in zip(clear_input_values, values[1:]):
        entry.delete(0, tk.END)
        entry.insert(0, value)

def update_student():
    """Update the selected student's record."""
    if selected_id is None:
        messagebox.showwarning("Select Student", "Select a student record first.")
        return

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()

    if not all([name, roll, course, email]):
        messagebox.showwarning("Missing Data", "Please fill in all fields.")
        return

    try:
        cursor.execute(
            """UPDATE students
               SET name = ?, roll_no = ?, course = ?, email = ?
               WHERE id = ?""",
            (name, roll, course, email, selected_id)
        )
        connection.commit()
        view_students()
        clear_fields()
        messagebox.showinfo("Success", "Student updated successfully.")

    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate Roll Number", "This roll number already exists.")

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))

def delete_student():
    """Delete the selected student's record."""
    if selected_id is None:
        messagebox.showwarning("Select Student", "Select a student record first.")
        return

    if not messagebox.askyesno("Confirm Delete", "Delete this student record?"):
        return

    try:
        cursor.execute("DELETE FROM students WHERE id = ?", (selected_id,))
        connection.commit()
        view_students()
        clear_fields()
        messagebox.showinfo("Success", "Student deleted successfully.")

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))

def close_app():
    """Close the database connection before exiting."""
    connection.close()
    window.destroy()

# Create the application window.
window = tk.Tk()
window.title("Student Management System")
window.geometry("900x600")
window.protocol("WM_DELETE_WINDOW", close_app)

# Input form.
form = ttk.LabelFrame(window, text="Student Details", padding=10)
form.pack(fill="x", padx=10, pady=10)

ttk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = ttk.Entry(form, width=28)
name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form, text="Roll Number:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
roll_entry = ttk.Entry(form, width=28)
roll_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(form, text="Course:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
course_entry = ttk.Entry(form, width=28)
course_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(form, text="Email:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
email_entry = ttk.Entry(form, width=28)
email_entry.grid(row=1, column=3, padx=5, pady=5)

# Action buttons.
actions = ttk.Frame(window)
actions.pack(fill="x", padx=10, pady=5)

ttk.Button(actions, text="Add Student", command=add_student).pack(side="left", padx=5)
ttk.Button(actions, text="View Students", command=view_students).pack(side="left", padx=5)
ttk.Button(actions, text="Update Student", command=update_student).pack(side="left", padx=5)
ttk.Button(actions, text="Delete Student", command=delete_student).pack(side="left", padx=5)
ttk.Button(actions, text="Clear Fields", command=clear_fields).pack(side="left", padx=5)

# Table displaying student records.
table_frame = ttk.Frame(window)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("id", "name", "roll_no", "course", "email")
student_table = ttk.Treeview(table_frame, columns=columns, show="headings")

for column, heading in zip(
    columns, ["ID", "Name", "Roll Number", "Course", "Email"]
):
    student_table.heading(column, text=heading)
    student_table.column(column, width=150)

student_table.pack(fill="both", expand=True)
student_table.bind("<<TreeviewSelect>>", select_student)

# Load existing records when the application starts.
view_students()

window.mainloop()
