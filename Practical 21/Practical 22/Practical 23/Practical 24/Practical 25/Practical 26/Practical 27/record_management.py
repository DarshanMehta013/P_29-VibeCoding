
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path

# Change this path if your practical folders are stored elsewhere.
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "Practical 25": BASE_DIR / "Practical 25" / "students.db",
    "Practical 26": BASE_DIR / "Practical 26" / "student_records.db",
}

selected_record = None


def connect(path):
    return sqlite3.connect(path)


def get_records():
    """Read records from both practical databases."""
    records = []

    for source, path in DATABASES.items():
        if not path.exists():
            continue

        try:
            with connect(path) as db:
                tables = {
                    row[0] for row in db.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    )
                }

                if source == "Practical 25" and "students" in tables:
                    rows = db.execute("""
                        SELECT id, name, roll_no, course, email
                        FROM students
                    """).fetchall()

                    for row in rows:
                        records.append(
                            (source, row[0], row[1], row[2],
                             row[3], row[4], "")
                        )

                elif source == "Practical 26" and "student_records" in tables:
                    rows = db.execute("""
                        SELECT id, full_name, roll_number, course, email, phone
                        FROM student_records
                    """).fetchall()

                    for row in rows:
                        records.append(
                            (source, row[0], row[1], row[2],
                             row[3], row[4], row[5])
                        )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error", f"{source}:\n{error}"
            )

    return records


def display_records():
    for item in table.get_children():
        table.delete(item)

    for source, record_id, name, roll, course, email, phone in get_records():
        table.insert(
            "", tk.END,
            values=(source, record_id, name, roll, course, email, phone)
        )


def select_record(event=None):
    global selected_record

    selection = table.selection()
    if not selection:
        return

    values = table.item(selection[0], "values")
    selected_record = (values[0], int(values[1]))

    fields = [name_entry, roll_entry, course_entry, email_entry, phone_entry]
    for field, value in zip(fields, values[2:]):
        field.delete(0, tk.END)
        field.insert(0, value)


def clear_fields():
    global selected_record
    for field in [name_entry, roll_entry, course_entry, email_entry, phone_entry]:
        field.delete(0, tk.END)

    selected_record = None
    table.selection_remove(table.selection())


def update_record():
    if selected_record is None:
        messagebox.showwarning("Select Record", "Please select a record first.")
        return

    source, record_id = selected_record
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if not all([name, roll, course, email]):
        messagebox.showwarning("Missing Details", "Fill in name, roll number, course and email.")
        return

    path = DATABASES[source]

    try:
        with connect(path) as db:
            if source == "Practical 25":
                db.execute("""
                    UPDATE students
                    SET name=?, roll_no=?, course=?, email=?
                    WHERE id=?
                """, (name, roll, course, email, record_id))
            else:
                db.execute("""
                    UPDATE student_records
                    SET full_name=?, roll_number=?, course=?, email=?, phone=?
                    WHERE id=?
                """, (name, roll, course, email, phone, record_id))

        display_records()
        clear_fields()
        messagebox.showinfo("Success", "Record updated successfully.")

    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate Roll Number", "That roll number already exists.")
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))


def delete_record():
    if selected_record is None:
        messagebox.showwarning("Select Record", "Please select a record first.")
        return

    source, record_id = selected_record

    if not messagebox.askyesno(
        "Confirm Deletion",
        f"Delete this record from {source}? This cannot be undone."
    ):
        return

    try:
        with connect(DATABASES[source]) as db:
            if source == "Practical 25":
                db.execute("DELETE FROM students WHERE id=?", (record_id,))
            else:
                db.execute(
                    "DELETE FROM student_records WHERE id=?", (record_id,)
                )

        display_records()
        clear_fields()
        messagebox.showinfo("Success", "Record deleted successfully.")

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))


# Main application window
root = tk.Tk()
root.title("Student Record Management System")
root.geometry("1050x600")
root.minsize(800, 450)

tk.Label(
    root, text="Student Record Management System",
    font=("Arial", 16, "bold")
).pack(pady=(10, 2))

tk.Label(
    root,
    text="Records are read from and saved to the original Practical 25 and 26 databases.",
    font=("Arial", 9)
).pack(pady=(0, 10))

form = ttk.Frame(root, padding=10)
form.pack(fill="x")

tk.Label(form, text="Name").grid(row=0, column=0, sticky="w", padx=5, pady=3)
name_entry = ttk.Entry(form)
name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

tk.Label(form, text="Roll Number").grid(row=1, column=0, sticky="w", padx=5, pady=3)
roll_entry = ttk.Entry(form)
roll_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=3)

tk.Label(form, text="Course / Branch").grid(row=2, column=0, sticky="w", padx=5, pady=3)
course_entry = ttk.Entry(form)
course_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=3)

tk.Label(form, text="Email").grid(row=3, column=0, sticky="w", padx=5, pady=3)
email_entry = ttk.Entry(form)
email_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=3)

tk.Label(form, text="Phone (if available)").grid(row=4, column=0, sticky="w", padx=5, pady=3)
phone_entry = ttk.Entry(form)
phone_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=3)

form.columnconfigure(1, weight=1)

buttons = ttk.Frame(root, padding=(10, 0))
buttons.pack(fill="x", pady=5)

ttk.Button(buttons, text="Display Records", command=display_records).pack(side="left", padx=4)
ttk.Button(buttons, text="Update Record", command=update_record).pack(side="left", padx=4)
ttk.Button(buttons, text="Delete Record", command=delete_record).pack(side="left", padx=4)
ttk.Button(buttons, text="Clear Fields", command=clear_fields).pack(side="left", padx=4)

table_frame = ttk.Frame(root, padding=10)
table_frame.pack(fill="both", expand=True)

columns = ("source", "id", "name", "roll", "course", "email", "phone")
table = ttk.Treeview(table_frame, columns=columns, show="headings")

headings = {
    "source": "Source",
    "id": "ID",
    "name": "Name",
    "roll": "Roll Number",
    "course": "Course / Branch",
    "email": "Email",
    "phone": "Phone"
}

for column, heading in headings.items():
    table.heading(column, text=heading)
    table.column(column, width=125, minwidth=75)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

table.bind("<<TreeviewSelect>>", select_record)

display_records()
root.mainloop()
