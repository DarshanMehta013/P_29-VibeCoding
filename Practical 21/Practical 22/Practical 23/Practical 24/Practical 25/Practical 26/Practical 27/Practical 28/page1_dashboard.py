"""
Practical 28 | Form 1: Dashboard
Run this file standalone to view and screenshot the Dashboard page.
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
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
    "secondary": "#0ea5e9",
    "success": "#10b981",
    "text_dark": "#0f172a",
    "text_muted": "#64748b",
}


class DashboardWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page 1: Dashboard | Student Record Management System")
        self.geometry("980x640")
        self.minsize(880, 560)
        self.configure(bg=THEME["content_bg"])

        self.db = DatabaseManager()
        self.setup_styles()
        self.create_layout()
        self.load_data()
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
            rowheight=30,
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

    def create_layout(self):
        # Top banner for Screenshot identification
        top_bar = tk.Frame(self, bg=THEME["header_bg"], height=60, padx=20)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        badge = tk.Label(top_bar, text="PRACTICAL 28", font=("Segoe UI", 9, "bold"), bg=THEME["primary"], fg="#ffffff", padx=8, pady=3)
        badge.pack(side=tk.LEFT, pady=16)

        title = tk.Label(top_bar, text="  Form 1 of 7 : Dashboard Overview", font=("Segoe UI", 13, "bold"), bg=THEME["header_bg"], fg="#ffffff")
        title.pack(side=tk.LEFT, pady=16)

        pill = tk.Label(top_bar, text="● SQLite Connected", font=("Segoe UI", 9, "bold"), bg="#ecfdf5", fg="#059669", padx=10, pady=3)
        pill.pack(side=tk.RIGHT, pady=18)

        # Main Body Container
        body = tk.Frame(self, bg=THEME["content_bg"], padx=24, pady=18)
        body.pack(fill=tk.BOTH, expand=True)

        # Hero Banner
        hero = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1, padx=20, pady=16)
        hero.pack(fill=tk.X, pady=(0, 16))

        tk.Label(hero, text="Welcome to Student Record Management System", font=("Segoe UI", 15, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w")
        tk.Label(hero, text="Main dashboard presenting key academic metrics, live student counts, and quick shortcuts.", font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"]).pack(anchor="w", pady=(3, 0))

        # KPI Stats Grid (3 Cards)
        stats = tk.Frame(body, bg=THEME["content_bg"])
        stats.pack(fill=tk.X, pady=(0, 16))
        stats.columnconfigure((0, 1, 2), weight=1, uniform="c")

        self.card_total = self.create_card(stats, 0, "👥", "Total Students", "0", "Live Count", THEME["primary"])
        self.card_courses = self.create_card(stats, 1, "🎓", "Total Courses", "0", "Programs", THEME["secondary"])
        self.card_status = self.create_card(stats, 2, "⚡", "Database Health", "Active", "SQLite3 OK", THEME["success"])

        # Quick Actions Strip
        actions = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1, padx=18, pady=12)
        actions.pack(fill=tk.X, pady=(0, 16))

        tk.Label(actions, text="Quick Actions:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 12))
        tk.Label(actions, text="[+ Add Student]   [📋 View All]   [✏️ Update]   [🗑️ Delete]   [🔍 Search]", font=("Segoe UI", 9), bg="#ffffff", fg=THEME["primary"]).pack(side=tk.LEFT)

        # Recent Registrations Card
        rec_card = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        rec_card.pack(fill=tk.BOTH, expand=True)

        rec_header = tk.Frame(rec_card, bg="#ffffff", padx=16, pady=10)
        rec_header.pack(fill=tk.X)
        tk.Label(rec_header, text="Recent Students Preview (Latest 5 Records)", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT)

        cols = ("roll", "name", "course", "email", "phone")
        self.tree = ttk.Treeview(rec_card, columns=cols, show="headings", style="Custom.Treeview", height=5)
        self.tree.heading("roll", text="Roll No")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("course", text="Course / Branch")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")

        self.tree.column("roll", width=100, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("course", width=180, anchor="w")
        self.tree.column("email", width=200, anchor="w")
        self.tree.column("phone", width=130, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 14))

    def create_card(self, parent, col, icon, title, val, badge, accent):
        card = tk.Frame(parent, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        card.grid(row=0, column=col, sticky="nsew", padx=6 if col == 1 else (0 if col == 0 else 6))

        inner = tk.Frame(card, bg="#ffffff", padx=16, pady=14)
        inner.pack(fill=tk.BOTH, expand=True)

        top = tk.Frame(inner, bg="#ffffff")
        top.pack(fill=tk.X)

        tk.Label(top, text=icon, font=("Segoe UI", 15), bg="#ffffff").pack(side=tk.LEFT)
        tk.Label(top, text=badge, font=("Segoe UI", 8, "bold"), bg="#f1f5f9", fg=accent, padx=6, pady=2).pack(side=tk.RIGHT)

        val_lbl = tk.Label(inner, text=val, font=("Segoe UI", 18, "bold"), bg="#ffffff", fg=accent)
        val_lbl.pack(anchor="w", pady=(6, 0))

        tk.Label(inner, text=title, font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"]).pack(anchor="w")
        return val_lbl

    def load_data(self):
        total_students = self.db.count_students()
        total_courses = self.db.count_courses()

        self.card_total.config(text=str(total_students))
        self.card_courses.config(text=str(total_courses))

        for row in self.db.get_recent_students(5):
            self.tree.insert("", tk.END, values=(row[1], row[2], row[3], row[4], row[5]))


if __name__ == "__main__":
    app = DashboardWindow()
    app.mainloop()
