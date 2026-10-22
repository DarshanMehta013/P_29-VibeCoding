"""
Practical 28 | Form 2: Add Student
Run this file standalone to view and screenshot the Add Student form.
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


class AddStudentWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page 2: Add Student | Student Record Management System")
        self.geometry("860x640")
        self.minsize(780, 560)
        self.configure(bg=THEME["content_bg"])

        self.db = DatabaseManager()
        self.create_layout()
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

        title = tk.Label(top_bar, text="  Form 2 of 7 : Add New Student Form", font=("Segoe UI", 13, "bold"), bg=THEME["header_bg"], fg="#ffffff")
        title.pack(side=tk.LEFT, pady=16)

        pill = tk.Label(top_bar, text="CRUD: CREATE", font=("Segoe UI", 9, "bold"), bg="#eff6ff", fg="#2563eb", padx=10, pady=3)
        pill.pack(side=tk.RIGHT, pady=18)

        # Body Container
        body = tk.Frame(self, bg=THEME["content_bg"], padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Header inside card
        header = tk.Frame(card, bg="#ffffff", padx=24, pady=18)
        header.pack(fill=tk.X)
        tk.Label(header, text="Student Registration Form", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w")
        tk.Label(header, text="Fill in all the required credentials. Roll number must be unique in SQLite.", font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"]).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(card, bg=THEME["card_border"], height=1)
        sep.pack(fill=tk.X)

        # Form Inputs Frame
        form = tk.Frame(card, bg="#ffffff", padx=30, pady=20)
        form.pack(fill=tk.BOTH, expand=True)
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        self.name_entry = self.add_field(form, 0, 0, "Student Full Name *", "e.g. Vivaan Sharma")
        self.roll_entry = self.add_field(form, 0, 1, "Roll Number * (Unique)", "e.g. 21")

        # Course Combobox
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
        self.combo_course.set("Computer Engineering")
        self.combo_course.pack(fill=tk.X, ipady=4)

        self.email_entry = self.add_field(form, 1, 1, "Email Address *", "e.g. student@gmail.com")
        self.phone_entry = self.add_field(form, 2, 0, "Phone Number * (10 Digits)", "e.g. 9876543210")

        # Pre-filled Demo Note
        tk.Label(form, text="💡 Tip: Enter details and click 'Save Student Record' to commit directly to SQLite.", font=("Segoe UI", 9, "italic"), bg="#ffffff", fg=THEME["text_muted"]).grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))

        # Status Label
        self.lbl_status = tk.Label(form, text="", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["success"])
        self.lbl_status.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(8, 0))

        # Buttons
        btn_box = tk.Frame(form, bg="#ffffff")
        btn_box.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=20)

        btn_save = tk.Button(
            btn_box,
            text="💾  Save Student Record",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.save_student
        )
        btn_save.pack(side=tk.LEFT, padx=(0, 12))

        btn_clear = tk.Button(
            btn_box,
            text="🔄  Clear Form",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.clear_form
        )
        btn_clear.pack(side=tk.LEFT)

    def add_field(self, parent, r, c, label, placeholder=""):
        f = tk.Frame(parent, bg="#ffffff")
        f.grid(row=r, column=c, sticky="ew", padx=10, pady=10)

        tk.Label(f, text=label, font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(0, 4))
        entry = tk.Entry(f, font=("Segoe UI", 10), bd=1, relief="solid")
        entry.pack(fill=tk.X, ipady=5)
        return entry

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.combo_course.set("Computer Engineering")
        self.lbl_status.config(text="")

    def save_student(self):
        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        course = self.combo_course.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not all([name, roll, course, email, phone]):
            messagebox.showwarning("Missing Details", "Please fill in all mandatory fields.")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return

        clean_phone = re.sub(r"\D", "", phone)
        if len(clean_phone) != 10:
            messagebox.showwarning("Invalid Phone", "Please enter a 10-digit mobile number.")
            return

        try:
            self.db.add_student(roll, name, course, email, clean_phone)
            self.lbl_status.config(text=f"✓ Success: Registered '{name}' (Roll: {roll}) to database.")
            messagebox.showinfo("Saved", f"Student '{name}' added successfully!")
            self.clear_form()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate Roll Number", f"Roll Number '{roll}' already exists in database.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = AddStudentWindow()
    app.mainloop()
