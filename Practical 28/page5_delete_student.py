"""
Practical 28 | Form 5: Delete Student
Run this file standalone to view and screenshot the Delete Student form.
"""

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
    "danger": "#ef4444",
    "text_dark": "#0f172a",
    "text_muted": "#64748b",
}


class DeleteStudentWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page 5: Delete Student | Student Record Management System")
        self.geometry("860x640")
        self.minsize(780, 560)
        self.configure(bg=THEME["content_bg"])

        self.db = DatabaseManager()
        self.selected_id = None
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

        badge = tk.Label(top_bar, text="PRACTICAL 28", font=("Segoe UI", 9, "bold"), bg=THEME["danger"], fg="#ffffff", padx=8, pady=3)
        badge.pack(side=tk.LEFT, pady=16)

        title = tk.Label(top_bar, text="  Form 5 of 7 : Delete Student Record", font=("Segoe UI", 13, "bold"), bg=THEME["header_bg"], fg="#ffffff")
        title.pack(side=tk.LEFT, pady=16)

        pill = tk.Label(top_bar, text="CRUD: DELETE", font=("Segoe UI", 9, "bold"), bg="#fee2e2", fg="#b91c1c", padx=10, pady=3)
        pill.pack(side=tk.RIGHT, pady=18)

        # Body Container
        body = tk.Frame(self, bg=THEME["content_bg"], padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(card, bg="#ffffff", padx=24, pady=18)
        header.pack(fill=tk.X)
        tk.Label(header, text="Delete Confirmation & Removal", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg=THEME["danger"]).pack(anchor="w")
        tk.Label(header, text="Select a student to inspect credentials. Action triggers a mandatory verification prompt.", font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"]).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(card, bg=THEME["card_border"], height=1)
        sep.pack(fill=tk.X)

        # Selection Bar
        lookup = tk.Frame(card, bg="#f8fafc", padx=20, pady=12, highlightbackground=THEME["card_border"], highlightthickness=1)
        lookup.pack(fill=tk.X, padx=20, pady=(16, 12))

        tk.Label(lookup, text="Select Student:", font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 10))

        self.combo_students = ttk.Combobox(lookup, font=("Segoe UI", 9), state="readonly", width=42)
        self.combo_students.pack(side=tk.LEFT, padx=(0, 8), ipady=3)
        self.combo_students.bind("<<ComboboxSelected>>", self.on_dropdown_select)

        # Preview Details Box
        preview_frame = tk.Frame(card, bg="#ffffff", padx=24, pady=14)
        preview_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(preview_frame, text="Selected Student Details (Verification Card):", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(0, 8))

        self.info_box = tk.Label(
            preview_frame,
            text="",
            font=("Segoe UI", 10),
            bg="#fff1f2",
            fg=THEME["text_dark"],
            justify=tk.LEFT,
            padx=20,
            pady=16,
            relief="solid",
            bd=1
        )
        self.info_box.pack(fill=tk.X, pady=(0, 20))

        # Action Buttons
        btn_box = tk.Frame(preview_frame, bg="#ffffff")
        btn_box.pack(anchor="w")

        self.btn_delete = tk.Button(
            btn_box,
            text="🗑️  Confirm & Delete Student Record",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["danger"],
            fg="#ffffff",
            relief="flat",
            padx=22,
            pady=9,
            cursor="hand2",
            command=self.confirm_and_delete
        )
        self.btn_delete.pack(side=tk.LEFT, padx=(0, 12))

        btn_cancel = tk.Button(
            btn_box,
            text="🔄  Reload List",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2",
            command=self.load_initial_student
        )
        btn_cancel.pack(side=tk.LEFT)

    def load_initial_student(self):
        records = self.db.get_all_students()
        options = [f"{r[1]} - {r[2]} ({r[3]})" for r in records]
        self.combo_students["values"] = options
        self.records_cache = records

        if records:
            self.combo_students.current(0)
            self.display_record(records[0])

    def on_dropdown_select(self, event=None):
        idx = self.combo_students.current()
        if idx >= 0 and idx < len(self.records_cache):
            self.display_record(self.records_cache[idx])

    def display_record(self, record):
        self.selected_id = record[0]
        self.current_record = record

        details = (
            f"  • Database Record ID:  {record[0]}\n"
            f"  • Roll Number:         {record[1]}\n"
            f"  • Full Student Name:   {record[2]}\n"
            f"  • Course / Branch:     {record[3]}\n"
            f"  • Email Address:       {record[4]}\n"
            f"  • Mobile Contact:      {record[5]}\n"
            f"  • Created At:          {record[6]}\n"
        )
        self.info_box.config(text=details, bg="#fff1f2", fg=THEME["text_dark"])

    def confirm_and_delete(self):
        if not self.selected_id or not hasattr(self, "current_record"):
            messagebox.showwarning("No Selection", "Please select a student record to delete.")
            return

        name = self.current_record[2]
        roll = self.current_record[1]

        ans = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete student record:\n\n"
            f"Name: {name}\nRoll No: {roll}\n\nThis cannot be undone!",
            icon="warning"
        )
        if ans:
            self.db.delete_student(self.selected_id)
            messagebox.showinfo("Deleted", f"Record for '{name}' was deleted successfully.")
            self.load_initial_student()


if __name__ == "__main__":
    app = DeleteStudentWindow()
    app.mainloop()
