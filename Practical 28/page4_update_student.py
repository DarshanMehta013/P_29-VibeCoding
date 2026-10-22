"""
Practical 28 | Form 4: Update Student
Run this file standalone to view and screenshot the Update Student form.
"""

import re
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from db import DatabaseManager

# Try setting DPI awareness for crisp Windows rendering
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

THEME = {
    "header_bg": "#1e293b",
    "content_bg": "#f8fafc",
    "card_bg": "#ffffff",
    "card_border": "#e2e8f0",
    "primary": "#4f46e5",
    "success": "#10b981",
    "text_dark": "#0f172a",
    "text_muted": "#64748b",
}


class UpdateStudentWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page 4: Update Student | Student Record Management System")
        self.geometry("880x660")
        self.minsize(800, 580)
        self.configure(bg=THEME["content_bg"])

        self.db = DatabaseManager()
        self.current_id = None
        self.create_layout()
        self.load_initial_student()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def create_layout(self):
        # Top banner for Screenshot identification
        top_bar = tk.Frame(self, bg=THEME["header_bg"], height=60, padx=20)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        badge = tk.Label(top_bar, text="PRACTICAL 28", font=("Segoe UI", 9, "bold"), bg=THEME["primary"], fg="#ffffff", padx=8, pady=3)
        badge.pack(side=tk.LEFT, pady=16)

        title = tk.Label(top_bar, text="  Form 4 of 7 : Update Student Record", font=("Segoe UI", 13, "bold"), bg=THEME["header_bg"], fg="#ffffff")
        title.pack(side=tk.LEFT, pady=16)

        pill = tk.Label(top_bar, text="CRUD: UPDATE", font=("Segoe UI", 9, "bold"), bg="#fef3c7", fg="#b45309", padx=10, pady=3)
        pill.pack(side=tk.RIGHT, pady=18)

        # Body Container
        body = tk.Frame(self, bg=THEME["content_bg"], padx=24, pady=18)
        body.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Selection Bar
        lookup = tk.Frame(card, bg="#f8fafc", padx=20, pady=12, highlightbackground=THEME["card_border"], highlightthickness=1)
        lookup.pack(fill=tk.X, padx=20, pady=(16, 12))

        tk.Label(lookup, text="Select Student to Edit:", font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 10))

        self.combo_students = ttk.Combobox(lookup, font=("Segoe UI", 9), state="readonly", width=42)
        self.combo_students.pack(side=tk.LEFT, padx=(0, 8), ipady=3)
        self.combo_students.bind("<<ComboboxSelected>>", self.on_dropdown_select)

        btn_load = tk.Button(lookup, text="Load Record", font=("Segoe UI", 9), bg="#e2e8f0", fg=THEME["text_dark"], relief="flat", padx=12, pady=4, cursor="hand2", command=self.on_dropdown_select)
        btn_load.pack(side=tk.LEFT)

        # Status Badge
        self.status_badge = tk.Label(card, text="", font=("Segoe UI", 9, "bold"), bg="#dbeafe", fg="#1e40af", padx=12, pady=6)
        self.status_badge.pack(fill=tk.X, padx=20, pady=(0, 12))

        # Form Edit Frame
        form = tk.Frame(card, bg="#ffffff", padx=20, pady=10)
        form.pack(fill=tk.BOTH, expand=True)
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        self.name_entry = self.add_field(form, 0, 0, "Student Full Name *")
        self.roll_entry = self.add_field(form, 0, 1, "Roll Number * (Unique)")

        c_frame = tk.Frame(form, bg="#ffffff")
        c_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        tk.Label(c_frame, text="Course / Department *", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(0, 4))
        self.combo_course = ttk.Combobox(
            c_frame,
            font=("Segoe UI", 10),
            state="readonly",
            values=[
                "Computer Engineering",
                "Information Technology",
                "Artificial Intelligence & DS",
                "Electronics & Comm. Engg.",
                "Mechanical Engineering",
                "Civil Engineering",
                "BCA (Computer Applications)",
                "MCA (Master of Comp. Apps.)",
            ]
        )
        self.combo_course.pack(fill=tk.X, ipady=4)

        self.email_entry = self.add_field(form, 1, 1, "Email Address *")
        self.phone_entry = self.add_field(form, 2, 0, "Phone Number * (10 Digits)")

        # Buttons
        btn_box = tk.Frame(form, bg="#ffffff")
        btn_box.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=20)

        btn_save = tk.Button(btn_box, text="💾  Save & Apply Changes", font=("Segoe UI", 10, "bold"), bg=THEME["primary"], fg="#ffffff", relief="flat", padx=20, pady=8, cursor="hand2", command=self.apply_update)
        btn_save.pack(side=tk.LEFT, padx=(0, 12))

        btn_reset = tk.Button(btn_box, text="🔄  Reset Form", font=("Segoe UI", 10), bg="#f1f5f9", fg=THEME["text_dark"], relief="flat", padx=18, pady=8, cursor="hand2", command=self.reset_form)
        btn_reset.pack(side=tk.LEFT)

    def add_field(self, parent, r, c, label):
        f = tk.Frame(parent, bg="#ffffff")
        f.grid(row=r, column=c, sticky="ew", padx=10, pady=10)
        tk.Label(f, text=label, font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(0, 4))
        entry = tk.Entry(f, font=("Segoe UI", 10), bd=1, relief="solid")
        entry.pack(fill=tk.X, ipady=5)
        return entry

    def load_initial_student(self):
        records = self.db.get_all_students()
        options = [f"{r[1]} - {r[2]} ({r[3]})" for r in records]
        self.combo_students["values"] = options
        self.records_cache = records

        if records:
            self.combo_students.current(0)
            self.populate(records[0])

    def on_dropdown_select(self, event=None):
        idx = self.combo_students.current()
        if idx >= 0 and idx < len(self.records_cache):
            self.populate(self.records_cache[idx])

    def populate(self, record):
        self.current_id = record[0]
        self.roll_entry.delete(0, tk.END)
        self.roll_entry.insert(0, record[1])

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, record[2])

        self.combo_course.set(record[3])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, record[4])

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, record[5])

        self.status_badge.config(
            text=f"Editing Active: {record[2]} | Roll No: {record[1]} (Database ID: {record[0]})",
            bg="#dbeafe",
            fg="#1e40af"
        )

    def reset_form(self):
        if self.current_id:
            rec = self.db.get_student_by_id(self.current_id)
            if rec:
                self.populate(rec)

    def apply_update(self):
        if not self.current_id:
            return

        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        course = self.combo_course.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not all([name, roll, course, email, phone]):
            messagebox.showwarning("Missing Details", "All fields are required.")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showwarning("Invalid Email", "Please enter a valid email format.")
            return

        clean_phone = re.sub(r"\D", "", phone)
        if len(clean_phone) != 10:
            messagebox.showwarning("Invalid Phone", "Please enter a valid 10-digit phone number.")
            return

        try:
            self.db.update_student(self.current_id, roll, name, course, email, clean_phone)
            self.status_badge.config(
                text=f"✓ Updated successfully: {name} (Roll: {roll})",
                bg="#ecfdf5",
                fg="#065f46"
            )
            messagebox.showinfo("Update Complete", f"Student '{name}' has been updated!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate Roll Number", "Roll number already assigned to another student.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = UpdateStudentWindow()
    app.mainloop()
