
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------- DATABASE ----------
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL,
    course TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT
)
""")
conn.commit()


# ---------- MAIN APPLICATION ----------
class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management System")
        self.root.geometry("1050x650")
        self.root.minsize(850, 550)

        self.selected_id = None
        self.fields = {}

        self.root.configure(bg="#F3F6FA")

        # Header
        header = tk.Frame(root, bg="#17365D", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="STUDENT RECORD MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#17365D"
        ).pack(pady=20)

        # Main layout
        body = tk.Frame(root, bg="#F3F6FA")
        body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(body, bg="#243B55", width=205)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=("Arial", 13, "bold"),
            bg="#243B55",
            fg="white"
        ).pack(pady=20)

        menus = [
            ("Dashboard", self.dashboard),
            ("Add Student", self.add_page),
            ("View Students", self.view_page),
            ("Update Student", self.update_page),
            ("Delete Student", self.delete_page),
            ("Search Student", self.search_page),
            ("About Project", self.about_page)
        ]

        for title, command in menus:
            tk.Button(
                self.sidebar,
                text=title,
                command=command,
                font=("Arial", 11),
                bg="#365879",
                fg="white",
                activebackground="#4F779D",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=18,
                pady=10
            ).pack(fill="x", padx=10, pady=4)

        tk.Button(
            self.sidebar,
            text="Exit Application",
            command=self.exit_app,
            bg="#B42318",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            pady=9
        ).pack(side="bottom", fill="x", padx=10, pady=15)

        self.content = tk.Frame(body, bg="#F3F6FA")
        self.content.pack(side="left", fill="both", expand=True)

        self.dashboard()

    # ---------- PAGE HELPER ----------
    def show_page(self, title):
        for widget in self.content.winfo_children():
            widget.destroy()

        self.fields = {}

        tk.Label(
            self.content,
            text=title,
            font=("Arial", 21, "bold"),
            bg="#F3F6FA",
            fg="#17365D"
        ).pack(anchor="w", padx=25, pady=(22, 12))

        return tk.Frame(self.content, bg="#F3F6FA")

    def button(self, parent, text, command, color="#2563A6"):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=14,
            pady=7,
            relief="flat"
        )

    def make_form(self, title):
        self.show_page(title)

        form = tk.Frame(self.content, bg="white", padx=25, pady=20)
        form.pack(fill="x", padx=25, pady=10)

        for field in ("Name", "Roll Number", "Course", "Email", "Phone"):
            row = tk.Frame(form, bg="white")
            row.pack(fill="x", pady=7)

            tk.Label(
                row,
                text=field + ":",
                width=15,
                anchor="w",
                font=("Arial", 11),
                bg="white"
            ).pack(side="left")

            entry = tk.Entry(row, font=("Arial", 11))
            entry.pack(side="left", fill="x", expand=True)
            self.fields[field] = entry

        return form

    def get_values(self):
        return {
            key: entry.get().strip()
            for key, entry in self.fields.items()
        }

    def valid(self, data):
        if not all(data[k] for k in
                   ("Name", "Roll Number", "Course", "Email")):
            messagebox.showwarning(
                "Missing Information",
                "Please fill in Name, Roll Number, Course and Email."
            )
            return False

        if "@" not in data["Email"] or "." not in data["Email"].split("@")[-1]:
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return False

        return True

    def clear_fields(self):
        for entry in self.fields.values():
            entry.delete(0, tk.END)

    # ---------- 1. DASHBOARD ----------
    def dashboard(self):
        self.show_page("Dashboard")

        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT course) FROM students")
        courses = cursor.fetchone()[0]

        for title, value in [
            ("Total Students", total),
            ("Courses Represented", courses),
            ("Database", "SQLite")
        ]:
            card = tk.Frame(
                self.content, bg="white",
                padx=25, pady=20, relief="groove", bd=1
            )
            card.pack(fill="x", padx=25, pady=10)

            tk.Label(
                card, text=title, font=("Arial", 13),
                bg="white", fg="#536579"
            ).pack(anchor="w")

            tk.Label(
                card, text=str(value), font=("Arial", 23, "bold"),
                bg="white", fg="#2563A6"
            ).pack(anchor="w", pady=(8, 0))

        tk.Label(
            self.content,
            text="Use the menu to manage student records.",
            font=("Arial", 12),
            bg="#F3F6FA"
        ).pack(anchor="w", padx=25, pady=15)

    # ---------- 2. ADD STUDENT ----------
    def add_page(self):
        form = self.make_form("Add Student")

        actions = tk.Frame(form, bg="white")
        actions.pack(pady=15)

        self.button(
            actions, "Save Student", self.save_student
        ).pack(side="left", padx=5)

        self.button(
            actions, "Clear Fields", self.clear_fields, "#64748B"
        ).pack(side="left", padx=5)

    def save_student(self):
        data = self.get_values()

        if not self.valid(data):
            return

        try:
            cursor.execute("""
                INSERT INTO students
                (name, roll_number, course, email, phone)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data["Name"], data["Roll Number"],
                data["Course"], data["Email"], data["Phone"]
            ))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            self.add_page()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate Roll Number",
                "This roll number already exists."
            )

    # ---------- TABLE HELPER ----------
    def make_table(self, parent, rows):
        columns = ("ID", "Name", "Roll Number",
                   "Course", "Email", "Phone")

        table_frame = tk.Frame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        table = ttk.Treeview(
            table_frame, columns=columns,
            show="headings", height=13
        )

        widths = (45, 150, 100, 120, 190, 110)

        for col, width in zip(columns, widths):
            table.heading(col, text=col)
            table.column(col, width=width, minwidth=45)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=table.yview
        )
        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for row in rows:
            table.insert("", "end", values=row)

        return table

    def fetch_students(self, search=""):
        cursor.execute("""
            SELECT id, name, roll_number, course, email, phone
            FROM students
            WHERE name LIKE ? OR roll_number LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%"))

        return cursor.fetchall()

    # ---------- 3. VIEW STUDENTS ----------
    def view_page(self):
        self.show_page("All Student Records")
        self.make_table(self.content, self.fetch_students())

    # ---------- 4. UPDATE STUDENT ----------
    def update_page(self):
        form = self.make_form("Update Student")

        tk.Label(
            form,
            text="Enter the existing Roll Number below, then click Load.",
            bg="white", fg="#536579", wraplength=550
        ).pack(anchor="w", pady=5)

        self.lookup = tk.Entry(form, font=("Arial", 11))
        self.lookup.pack(fill="x", pady=5)

        actions = tk.Frame(form, bg="white")
        actions.pack(pady=12)

        self.button(
            actions, "Load Record", self.load_student
        ).pack(side="left", padx=5)

        self.button(
            actions, "Update Record", self.update_student, "#16805D"
        ).pack(side="left", padx=5)

    def load_student(self):
        roll = self.lookup.get().strip()

        cursor.execute("""
            SELECT id, name, roll_number, course, email, phone
            FROM students WHERE roll_number = ?
        """, (roll,))

        row = cursor.fetchone()

        if not row:
            self.selected_id = None
            messagebox.showerror("Not Found", "Student not found.")
            return

        self.selected_id = row[0]

        for key, value in zip(
            self.fields.keys(), row[1:]
        ):
            self.fields[key].delete(0, tk.END)
            self.fields[key].insert(0, value or "")

        messagebox.showinfo("Loaded", "Student record loaded.")

    def update_student(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Select Record", "Load a student record first."
            )
            return

        data = self.get_values()

        if not self.valid(data):
            return

        try:
            cursor.execute("""
                UPDATE students
                SET name=?, roll_number=?, course=?, email=?, phone=?
                WHERE id=?
            """, (
                data["Name"], data["Roll Number"],
                data["Course"], data["Email"], data["Phone"],
                self.selected_id
            ))
            conn.commit()
            self.selected_id = None

            messagebox.showinfo("Success", "Student updated successfully!")
            self.update_page()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate Roll Number",
                "Another student already uses this roll number."
            )

    # ---------- 5. DELETE STUDENT ----------
    def delete_page(self):
        self.show_page("Delete Student")

        tk.Label(
            self.content,
            text="Select a student record and click Delete Selected.",
            font=("Arial", 11), bg="#F3F6FA"
        ).pack(anchor="w", padx=25)

        table = self.make_table(
            self.content, self.fetch_students()
        )

        def delete_selected():
            selected = table.selection()

            if not selected:
                messagebox.showwarning(
                    "Selection Required",
                    "Please select a student record."
                )
                return

            row = table.item(selected[0])["values"]

            if messagebox.askyesno(
                "Confirm Deletion",
                f"Delete student {row[1]} (Roll No. {row[2]})?"
            ):
                cursor.execute(
                    "DELETE FROM students WHERE id = ?", (row[0],)
                )
                conn.commit()
                messagebox.showinfo("Success", "Record deleted.")
                self.delete_page()

        self.button(
            self.content, "Delete Selected",
            delete_selected, "#B42318"
        ).pack(anchor="w", padx=25, pady=10)

    # ---------- 6. SEARCH STUDENT ----------
    def search_page(self):
        self.show_page("Search Student")

        search_frame = tk.Frame(self.content, bg="white", padx=20, pady=15)
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            search_frame,
            text="Name or Roll Number:",
            font=("Arial", 11), bg="white"
        ).pack(side="left", padx=5)

        search_entry = tk.Entry(search_frame, font=("Arial", 11))
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        table_holder = tk.Frame(self.content, bg="#F3F6FA")
        table_holder.pack(fill="both", expand=True)

        def perform_search():
            for widget in table_holder.winfo_children():
                widget.destroy()

            term = search_entry.get().strip()
            results = self.fetch_students(term)

            self.make_table(table_holder, results)

            if not results:
                messagebox.showinfo(
                    "No Results", "No matching student records found."
                )

        self.button(
            search_frame, "Search", perform_search
        ).pack(side="left", padx=5)

        search_entry.bind("<Return>", lambda event: perform_search())
        self.make_table(table_holder, self.fetch_students())

    # ---------- 7. ABOUT PROJECT ----------
    def about_page(self):
        self.show_page("About Project")

        info = tk.Frame(self.content, bg="white", padx=30, pady=25)
        info.pack(fill="x", padx=25, pady=15)

        details = [
            ("Project Name", "Student Record Management System"),
            ("Developer", "Darshan Mehta"),
            ("Programming Language", "Python"),
            ("GUI Library", "Tkinter"),
            ("Database", "SQLite"),
            ("Main Features", "Create, Read, Update, Delete and Search"),
            ("Development Method", "AI-assisted code generation")
        ]

        for label, value in details:
            tk.Label(
                info, text=label + ":",
                font=("Arial", 11, "bold"),
                bg="white", anchor="w", width=20
            ).pack(anchor="w", pady=5)

            tk.Label(
                info, text=value,
                font=("Arial", 11), bg="white",
                anchor="w", wraplength=550
            ).pack(anchor="w", padx=10, pady=(0, 8))

    # ---------- EXIT ----------
    def exit_app(self):
        if messagebox.askyesno(
            "Exit", "Are you sure you want to exit?"
        ):
            conn.commit()
            conn.close()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
