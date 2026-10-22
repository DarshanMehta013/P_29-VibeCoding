"""
Practical 28 | Form 6: Search Student
Run this file standalone to view and screenshot the Search Student form.
"""

import tkinter as tk
from tkinter import ttk
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
    "text_dark": "#0f172a",
    "text_muted": "#64748b",
}


class SearchStudentWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page 6: Search Student | Student Record Management System")
        self.geometry("980x640")
        self.minsize(860, 560)
        self.configure(bg=THEME["content_bg"])

        self.db = DatabaseManager()
        self.setup_styles()
        self.create_layout()
        self.perform_search()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Custom.Treeview",
            background="#ffffff",
            foreground=THEME["text_dark"],
            rowheight=32,
            fieldbackground="#ffffff",
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Custom.Treeview.Heading",
            background="#f1f5f9",
            foreground=THEME["text_dark"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(8, 8)
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", THEME["primary"])],
            foreground=[("selected", "#ffffff")]
        )

    def create_layout(self):
        # Top banner for Screenshot identification
        top_bar = tk.Frame(self, bg=THEME["header_bg"], height=60, padx=20)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        badge = tk.Label(top_bar, text="PRACTICAL 28", font=("Segoe UI", 9, "bold"), bg=THEME["primary"], fg="#ffffff", padx=8, pady=3)
        badge.pack(side=tk.LEFT, pady=16)

        title = tk.Label(top_bar, text="  Form 6 of 7 : Search Student Records", font=("Segoe UI", 13, "bold"), bg=THEME["header_bg"], fg="#ffffff")
        title.pack(side=tk.LEFT, pady=16)

        pill = tk.Label(top_bar, text="FILTER & QUERY ENGINE", font=("Segoe UI", 9, "bold"), bg="#eff6ff", fg="#1d4ed8", padx=10, pady=3)
        pill.pack(side=tk.RIGHT, pady=18)

        # Body Container
        body = tk.Frame(self, bg=THEME["content_bg"], padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(card, bg="#ffffff", padx=20, pady=14)
        header.pack(fill=tk.X)
        tk.Label(header, text="Search & Filter Database", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w")
        tk.Label(header, text="Real-time lookup by Name, Roll Number, or Course with instant tabular rendering.", font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"]).pack(anchor="w", pady=(2, 0))

        # Search Controls Strip
        controls = tk.Frame(card, bg="#f8fafc", padx=20, pady=14, highlightbackground=THEME["card_border"], highlightthickness=1)
        controls.pack(fill=tk.X, padx=20, pady=(0, 12))

        # Top row: Search input + Buttons
        row1 = tk.Frame(controls, bg="#f8fafc")
        row1.pack(fill=tk.X)

        tk.Label(row1, text="Search Query:", font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 10))

        self.search_entry = tk.Entry(row1, font=("Segoe UI", 10), bd=1, relief="solid")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4)
        self.search_entry.bind("<KeyRelease>", lambda e: self.perform_search())

        btn_search = tk.Button(row1, text="🔍 Search", font=("Segoe UI", 9, "bold"), bg=THEME["primary"], fg="#ffffff", relief="flat", padx=16, pady=4, cursor="hand2", command=self.perform_search)
        btn_search.pack(side=tk.LEFT, padx=(0, 6))

        btn_reset = tk.Button(row1, text="Reset", font=("Segoe UI", 9), bg="#e2e8f0", fg=THEME["text_dark"], relief="flat", padx=12, pady=4, cursor="hand2", command=self.reset_search)
        btn_reset.pack(side=tk.LEFT)

        # Bottom row: Radio filters
        row2 = tk.Frame(controls, bg="#f8fafc")
        row2.pack(fill=tk.X, pady=(10, 0))

        tk.Label(row2, text="Criteria:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg=THEME["text_muted"]).pack(side=tk.LEFT, padx=(0, 10))

        self.filter_var = tk.StringVar(value="all")
        for text, val in [("All Fields", "all"), ("Roll Number", "roll"), ("Name", "name"), ("Course", "course")]:
            tk.Radiobutton(
                row2,
                text=text,
                variable=self.filter_var,
                value=val,
                bg="#f8fafc",
                font=("Segoe UI", 9),
                command=self.perform_search
            ).pack(side=tk.LEFT, padx=6)

        # Status Badge
        self.results_badge = tk.Label(card, text="", font=("Segoe UI", 9, "italic"), bg="#ffffff", fg=THEME["text_muted"], padx=20)
        self.results_badge.pack(anchor="w", pady=(0, 8))

        # Results Table
        table_frame = tk.Frame(card, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        cols = ("id", "roll", "name", "course", "email", "phone")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Custom.Treeview")

        self.tree.heading("id", text="ID")
        self.tree.heading("roll", text="Roll No")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("course", text="Course / Dept")
        self.tree.heading("email", text="Email Address")
        self.tree.heading("phone", text="Phone Number")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("roll", width=100, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("course", width=190, anchor="w")
        self.tree.column("email", width=200, anchor="w")
        self.tree.column("phone", width=130, anchor="center")

        scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.filter_var.set("all")
        self.perform_search()

    def perform_search(self):
        q = self.search_entry.get().strip()
        criteria = self.filter_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not q:
            records = self.db.get_all_students()
            self.results_badge.config(text=f"Showing all {len(records)} records in database.")
        else:
            records = self.db.search_students(q, field=criteria)
            self.results_badge.config(text=f"Found {len(records)} matching student(s) for query '{q}'.")

        for idx, r in enumerate(records):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4], r[5]), tags=(tag,))

        self.tree.tag_configure("even", background="#ffffff")
        self.tree.tag_configure("odd", background="#f8fafc")


if __name__ == "__main__":
    app = SearchStudentWindow()
    app.mainloop()
