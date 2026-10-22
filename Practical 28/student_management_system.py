"""
Practical 28: Student Record Management System
Desktop CRUD Mini Project with 7 Integrated Pages/Forms
GUI: Tkinter + ttk
Database: SQLite3
AI-Assisted Architecture
"""

import os
import re
import csv
import sqlite3
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Try setting DPI awareness for crisp Windows rendering
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Determine database path
CURRENT_DIR = Path(__file__).resolve().parent
DB_PATH = CURRENT_DIR / "student_records.db"

# Color Palette (Modern Slate & Indigo Theme)
THEME = {
    "sidebar_bg": "#1e293b",       # Dark Slate
    "sidebar_hover": "#334155",    # Slate hover
    "sidebar_active": "#4f46e5",   # Vibrant Indigo
    "sidebar_text": "#e2e8f0",     # Light text
    "sidebar_subtext": "#94a3b8",  # Muted text
    "header_bg": "#ffffff",        # White header
    "content_bg": "#f8fafc",       # Off-white / light grey
    "card_bg": "#ffffff",          # Pure white cards
    "card_border": "#e2e8f0",      # Card border
    "primary": "#4f46e5",          # Primary Indigo
    "primary_hover": "#4338ca",
    "secondary": "#0ea5e9",        # Sky Blue
    "success": "#10b981",          # Emerald Green
    "warning": "#f59e0b",          # Amber
    "danger": "#ef4444",           # Crimson Red
    "text_dark": "#0f172a",        # Slate 900
    "text_muted": "#64748b",       # Slate 500
}


class DatabaseManager:
    """Handles all SQLite database CRUD operations."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_no TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    course TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

        # Seed initial sample data if empty
        if self.count_students() == 0:
            sample_data = [
                ("21", "Vivaan Sharma", "Computer Engineering", "vivaan@gmail.com", "9876543210", "2026-10-15 10:30:00"),
                ("55", "Meet Patel", "Computer Engineering", "meet@gmail.com", "9876543211", "2026-10-16 11:45:00"),
                ("101", "Aarav Gupta", "Information Technology", "aarav@gmail.com", "9823456789", "2026-10-18 09:15:00"),
                ("102", "Diya Shah", "Artificial Intelligence", "diya@gmail.com", "9812345678", "2026-10-20 14:20:00"),
                ("103", "Rohan Verma", "Data Science", "rohan@gmail.com", "9898765432", "2026-10-21 16:05:00"),
            ]
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany("""
                    INSERT INTO students (roll_no, name, course, email, phone, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, sample_data)
                conn.commit()

    def count_students(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            return cursor.fetchone()[0]

    def count_courses(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT course) FROM students")
            return cursor.fetchone()[0]

    def get_all_students(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students ORDER BY id DESC")
            return cursor.fetchall()

    def get_recent_students(self, limit=5):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students ORDER BY id DESC LIMIT ?", (limit,))
            return cursor.fetchall()

    def get_student_by_roll(self, roll_no):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE roll_no = ?", (roll_no,))
            return cursor.fetchone()

    def get_student_by_id(self, student_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE id = ?", (student_id,))
            return cursor.fetchone()

    def add_student(self, roll_no, name, course, email, phone):
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (roll_no, name, course, email, phone, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (roll_no, name, course, email, phone, created_at))
            conn.commit()
            return cursor.lastrowid

    def update_student(self, student_id, roll_no, name, course, email, phone):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students
                SET roll_no = ?, name = ?, course = ?, email = ?, phone = ?
                WHERE id = ?
            """, (roll_no, name, course, email, phone, student_id))
            conn.commit()
            return cursor.rowcount

    def delete_student(self, student_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            return cursor.rowcount

    def search_students(self, query, field="all"):
        q = f"%{query.strip()}%"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if field == "roll":
                cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE roll_no LIKE ? ORDER BY id DESC", (q,))
            elif field == "name":
                cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE name LIKE ? ORDER BY id DESC", (q,))
            elif field == "course":
                cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE course LIKE ? ORDER BY id DESC", (q,))
            else:
                cursor.execute("""
                    SELECT id, roll_no, name, course, email, phone, created_at
                    FROM students
                    WHERE roll_no LIKE ? OR name LIKE ? OR course LIKE ? OR email LIKE ? OR phone LIKE ?
                    ORDER BY id DESC
                """, (q, q, q, q, q))
            return cursor.fetchall()


class StudentManagementApp(tk.Tk):
    """Main Application Window with Sidebar & 7 Forms/Pages."""

    def __init__(self):
        super().__init__()
        self.title("Student Record Management System | Program No. 28")
        self.geometry("1100x700")
        self.minsize(980, 620)
        self.configure(bg=THEME["content_bg"])

        # Initialize Database Manager
        self.db = DatabaseManager()

        # Shared state for selection between pages
        self.shared_student_id = None

        # Configure TTK Styles
        self.setup_styles()

        # Create Layout Structure
        self.create_layout()

        # Build All 7 Forms / Pages
        self.pages = {}
        self.create_pages()

        # Show Dashboard initially
        self.show_page("Dashboard")

        # Center Window on Screen
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Global Treeview style
        self.style.configure(
            "Custom.Treeview",
            background="#ffffff",
            foreground=THEME["text_dark"],
            rowheight=30,
            fieldbackground="#ffffff",
            font=("Segoe UI", 10),
            borderwidth=0
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            background="#f1f5f9",
            foreground=THEME["text_dark"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(8, 8)
        )
        self.style.map(
            "Custom.Treeview",
            background=[("selected", THEME["primary"])],
            foreground=[("selected", "#ffffff")]
        )
        self.style.map(
            "Custom.Treeview.Heading",
            background=[("active", "#e2e8f0")]
        )

        # Combobox style
        self.style.configure("Custom.TCombobox", padding=5, font=("Segoe UI", 10))

    def create_layout(self):
        # Master container
        self.sidebar_frame = tk.Frame(self, bg=THEME["sidebar_bg"], width=240)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        # Right container (Header + Dynamic Page Area)
        self.right_container = tk.Frame(self, bg=THEME["content_bg"])
        self.right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Top Header Bar
        self.header_bar = tk.Frame(self.right_container, bg=THEME["header_bg"], height=64, padx=24)
        self.header_bar.pack(side=tk.TOP, fill=tk.X)
        self.header_bar.pack_propagate(False)

        # Header Title
        self.header_title = tk.Label(
            self.header_bar,
            text="Dashboard Overview",
            font=("Segoe UI", 15, "bold"),
            bg=THEME["header_bg"],
            fg=THEME["text_dark"]
        )
        self.header_title.pack(side=tk.LEFT, pady=16)

        # Header Right Stats Pill & Clock
        self.header_pill = tk.Label(
            self.header_bar,
            text="● Live Database Connected",
            font=("Segoe UI", 9, "bold"),
            bg="#ecfdf5",
            fg="#059669",
            padx=12,
            pady=4
        )
        self.header_pill.pack(side=tk.RIGHT, pady=18)

        # Separator line under header
        header_sep = tk.Frame(self.right_container, bg=THEME["card_border"], height=1)
        header_sep.pack(side=tk.TOP, fill=tk.X)

        # Main Dynamic Content Area
        self.content_area = tk.Frame(self.right_container, bg=THEME["content_bg"], padx=24, pady=20)
        self.content_area.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Build Sidebar Contents
        self.build_sidebar()

    def build_sidebar(self):
        # Brand / Logo Header
        brand_frame = tk.Frame(self.sidebar_frame, bg=THEME["sidebar_bg"], padx=18, pady=22)
        brand_frame.pack(fill=tk.X)

        logo_badge = tk.Label(
            brand_frame,
            text="SRMS",
            font=("Segoe UI", 11, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            padx=8,
            pady=4
        )
        logo_badge.pack(side=tk.LEFT, padx=(0, 10))

        title_container = tk.Frame(brand_frame, bg=THEME["sidebar_bg"])
        title_container.pack(side=tk.LEFT, fill=tk.X)

        app_title = tk.Label(
            title_container,
            text="Student Portal",
            font=("Segoe UI", 12, "bold"),
            bg=THEME["sidebar_bg"],
            fg="#ffffff"
        )
        app_title.pack(anchor="w")

        app_subtitle = tk.Label(
            title_container,
            text="CRUD System v1.0",
            font=("Segoe UI", 8),
            bg=THEME["sidebar_bg"],
            fg=THEME["sidebar_subtext"]
        )
        app_subtitle.pack(anchor="w")

        # Sidebar Separator
        sep = tk.Frame(self.sidebar_frame, bg="#334155", height=1)
        sep.pack(fill=tk.X, padx=16, pady=(0, 12))

        # Menu section label
        menu_label = tk.Label(
            self.sidebar_frame,
            text="NAVIGATION MENU",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["sidebar_bg"],
            fg="#64748b",
            padx=20,
            pady=4
        )
        menu_label.pack(anchor="w")

        # Navigation Buttons (7 Pages)
        self.nav_items = [
            ("Dashboard", "  🏠  Dashboard"),
            ("Add Student", "  ➕  Add Student"),
            ("View Students", "  📋  View Students"),
            ("Update Student", "  ✏️   Update Student"),
            ("Delete Student", "  🗑️   Delete Student"),
            ("Search Student", "  🔍  Search Student"),
            ("About", "  ℹ️   About Project"),
        ]

        self.nav_buttons = {}
        for page_key, display_text in self.nav_items:
            btn = tk.Button(
                self.sidebar_frame,
                text=display_text,
                font=("Segoe UI", 10),
                anchor="w",
                bg=THEME["sidebar_bg"],
                fg=THEME["sidebar_text"],
                activebackground=THEME["sidebar_hover"],
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                padx=20,
                pady=10,
                cursor="hand2",
                command=lambda k=page_key: self.show_page(k)
            )
            btn.pack(fill=tk.X, pady=1)
            self.nav_buttons[page_key] = btn

        # Sidebar Footer
        footer_frame = tk.Frame(self.sidebar_frame, bg=THEME["sidebar_bg"], padx=18, pady=16)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        quick_db_info = tk.Label(
            footer_frame,
            text="SQLite3 • Embedded DB\nProgram No. 28 Mini Project",
            font=("Segoe UI", 8),
            bg=THEME["sidebar_bg"],
            fg=THEME["sidebar_subtext"],
            justify=tk.LEFT
        )
        quick_db_info.pack(anchor="w")

    def create_pages(self):
        """Construct the 7 form/page instances."""
        self.pages["Dashboard"] = DashboardPage(self.content_area, self)
        self.pages["Add Student"] = AddStudentPage(self.content_area, self)
        self.pages["View Students"] = ViewStudentsPage(self.content_area, self)
        self.pages["Update Student"] = UpdateStudentPage(self.content_area, self)
        self.pages["Delete Student"] = DeleteStudentPage(self.content_area, self)
        self.pages["Search Student"] = SearchStudentPage(self.content_area, self)
        self.pages["About"] = AboutPage(self.content_area, self)

        for p in self.pages.values():
            p.grid(row=0, column=0, sticky="nsew")

        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

    def show_page(self, page_name):
        """Switch active page and update sidebar styling."""
        page = self.pages.get(page_name)
        if not page:
            return

        # Bring frame to front
        page.tkraise()

        # Call on_show hook if page has one
        if hasattr(page, "on_show"):
            page.on_show()

        # Update header title
        self.header_title.config(text=f"{page_name}")

        # Update sidebar button states
        for key, btn in self.nav_buttons.items():
            if key == page_name:
                btn.config(bg=THEME["sidebar_active"], fg="#ffffff", font=("Segoe UI", 10, "bold"))
            else:
                btn.config(bg=THEME["sidebar_bg"], fg=THEME["sidebar_text"], font=("Segoe UI", 10))

    def navigate_to_update(self, student_id):
        """Navigate to update page with a preselected student ID."""
        self.shared_student_id = student_id
        self.show_page("Update Student")
        update_page = self.pages["Update Student"]
        update_page.load_student_by_id(student_id)

    def navigate_to_delete(self, student_id):
        """Navigate to delete page with a preselected student ID."""
        self.shared_student_id = student_id
        self.show_page("Delete Student")
        delete_page = self.pages["Delete Student"]
        delete_page.load_student_by_id(student_id)


# ==============================================================================
# 1. DASHBOARD PAGE
# ==============================================================================
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        # Hero Banner
        hero_card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        hero_card.pack(fill=tk.X, pady=(0, 16))

        hero_inner = tk.Frame(hero_card, bg="#ffffff", padx=24, pady=20)
        hero_inner.pack(fill=tk.X)

        hero_title = tk.Label(
            hero_inner,
            text="Welcome to Student Record Management System",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff",
            fg=THEME["text_dark"]
        )
        hero_title.pack(anchor="w")

        hero_desc = tk.Label(
            hero_inner,
            text="A full-featured desktop CRUD mini project integrating Tkinter GUI, SQLite3 database, and AI-assisted workflow.",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg=THEME["text_muted"]
        )
        hero_desc.pack(anchor="w", pady=(4, 0))

        # KPI Stats Cards Grid (3 Cards)
        stats_frame = tk.Frame(self, bg=THEME["content_bg"])
        stats_frame.pack(fill=tk.X, pady=(0, 16))
        stats_frame.columnconfigure((0, 1, 2), weight=1, uniform="stat_cards")

        # Card 1: Total Students
        self.card_total = self.create_stat_card(
            stats_frame,
            col=0,
            icon="👥",
            title="Total Registered Students",
            val_text="0",
            badge="Live Count",
            accent="#4f46e5"
        )

        # Card 2: Total Courses
        self.card_courses = self.create_stat_card(
            stats_frame,
            col=1,
            icon="🎓",
            title="Enrolled Departments / Courses",
            val_text="0",
            badge="Programs",
            accent="#0ea5e9"
        )

        # Card 3: System Status
        self.card_status = self.create_stat_card(
            stats_frame,
            col=2,
            icon="⚡",
            title="Database Health",
            val_text="Active",
            badge="SQLite3 OK",
            accent="#10b981"
        )

        # Middle Row: Quick Actions Bar
        actions_card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1, padx=20, pady=14)
        actions_card.pack(fill=tk.X, pady=(0, 16))

        action_label = tk.Label(actions_card, text="Quick Shortcuts:", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"])
        action_label.pack(side=tk.LEFT, padx=(0, 12))

        btn_add = tk.Button(
            actions_card,
            text="➕  Add New Student",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.controller.show_page("Add Student")
        )
        btn_add.pack(side=tk.LEFT, padx=6)

        btn_view = tk.Button(
            actions_card,
            text="📋  View All Records",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.controller.show_page("View Students")
        )
        btn_view.pack(side=tk.LEFT, padx=6)

        btn_search = tk.Button(
            actions_card,
            text="🔍  Search Database",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.controller.show_page("Search Student")
        )
        btn_search.pack(side=tk.LEFT, padx=6)

        # Bottom Section: Recent Students Preview Card
        table_card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        table_card.pack(fill=tk.BOTH, expand=True)

        header_box = tk.Frame(table_card, bg="#ffffff", padx=20, pady=12)
        header_box.pack(fill=tk.X)

        tk.Label(
            header_box,
            text="Recently Enrolled Students (Latest 5)",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg=THEME["text_dark"]
        ).pack(side=tk.LEFT)

        # Preview Table
        cols = ("roll", "name", "course", "email", "phone")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", style="Custom.Treeview", height=5)
        self.tree.heading("roll", text="Roll Number")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("course", text="Course / Branch")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")

        self.tree.column("roll", width=120, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("course", width=200, anchor="w")
        self.tree.column("email", width=220, anchor="w")
        self.tree.column("phone", width=140, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

    def create_stat_card(self, parent, col, icon, title, val_text, badge, accent):
        card = tk.Frame(parent, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        card.grid(row=0, column=col, sticky="nsew", padx=6 if col == 1 else (0 if col == 0 else 6))

        inner = tk.Frame(card, bg="#ffffff", padx=18, pady=16)
        inner.pack(fill=tk.BOTH, expand=True)

        top_row = tk.Frame(inner, bg="#ffffff")
        top_row.pack(fill=tk.X)

        icon_lbl = tk.Label(top_row, text=icon, font=("Segoe UI", 16), bg="#ffffff")
        icon_lbl.pack(side=tk.LEFT)

        badge_lbl = tk.Label(
            top_row,
            text=badge,
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9",
            fg=accent,
            padx=8,
            pady=2
        )
        badge_lbl.pack(side=tk.RIGHT)

        val_lbl = tk.Label(inner, text=val_text, font=("Segoe UI", 20, "bold"), bg="#ffffff", fg=accent)
        val_lbl.pack(anchor="w", pady=(8, 0))

        title_lbl = tk.Label(inner, text=title, font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"])
        title_lbl.pack(anchor="w")

        return val_lbl

    def on_show(self):
        """Refresh dashboard statistics and recent table."""
        total_students = self.controller.db.count_students()
        total_courses = self.controller.db.count_courses()

        self.card_total.config(text=str(total_students))
        self.card_courses.config(text=str(total_courses))

        # Clear and reload recent students
        for item in self.tree.get_children():
            self.tree.delete(item)

        recent = self.controller.db.get_recent_students(5)
        for row in recent:
            # row: id, roll_no, name, course, email, phone, created_at
            self.tree.insert("", tk.END, values=(row[1], row[2], row[3], row[4], row[5]))


# ==============================================================================
# 2. ADD STUDENT PAGE
# ==============================================================================
class AddStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(card, bg="#ffffff", padx=24, pady=20)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Add New Student Record",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg=THEME["text_dark"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Please fill in all student credentials. Roll number must be unique.",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_muted"]
        ).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(card, bg=THEME["card_border"], height=1)
        sep.pack(fill=tk.X)

        # Form Container
        form_frame = tk.Frame(card, bg="#ffffff", padx=30, pady=24)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Grid layout for fields
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

        # 1. Full Name
        self.entry_name = self.create_form_field(form_frame, row=0, col=0, label="Full Name *", placeholder="e.g. Vivaan Sharma")

        # 2. Roll Number
        self.entry_roll = self.create_form_field(form_frame, row=0, col=1, label="Roll Number * (Unique)", placeholder="e.g. 21 or CS2026-05")

        # 3. Course / Branch (Combobox)
        course_frame = tk.Frame(form_frame, bg="#ffffff")
        course_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(course_frame, text="Course / Department *", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(0, 5))
        self.combo_course = ttk.Combobox(
            course_frame,
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

        # 4. Email
        self.entry_email = self.create_form_field(form_frame, row=1, col=1, label="Email Address *", placeholder="e.g. vivaan@gmail.com")

        # 5. Phone Number
        self.entry_phone = self.create_form_field(form_frame, row=2, col=0, label="Phone Number * (10 Digits)", placeholder="e.g. 9876543210")

        # Status / Feedback Banner
        self.feedback_lbl = tk.Label(
            form_frame,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg="#ffffff",
            fg=THEME["primary"]
        )
        self.feedback_lbl.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(12, 0))

        # Buttons Row
        btn_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_frame.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=20)

        btn_save = tk.Button(
            btn_frame,
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
            btn_frame,
            text="🔄  Clear Form",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.clear_fields
        )
        btn_clear.pack(side=tk.LEFT, padx=(0, 12))

        btn_view = tk.Button(
            btn_frame,
            text="📋  View All Students",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=THEME["primary"],
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=lambda: self.controller.show_page("View Students")
        )
        btn_view.pack(side=tk.LEFT)

    def create_form_field(self, parent, row, col, label, placeholder=""):
        f = tk.Frame(parent, bg="#ffffff")
        f.grid(row=row, column=col, sticky="ew", padx=10, pady=10)

        lbl = tk.Label(f, text=label, font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"])
        lbl.pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(f, font=("Segoe UI", 10), bd=1, relief="solid", highlightthickness=1, highlightcolor=THEME["primary"])
        entry.pack(fill=tk.X, ipady=5)
        return entry

    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_roll.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.combo_course.set("Computer Engineering")
        self.feedback_lbl.config(text="")

    def save_student(self):
        name = self.entry_name.get().strip()
        roll = self.entry_roll.get().strip()
        course = self.combo_course.get().strip()
        email = self.entry_email.get().strip()
        phone = self.entry_phone.get().strip()

        # Validation
        if not all([name, roll, course, email, phone]):
            messagebox.showwarning("Incomplete Form", "Please fill in all mandatory fields.")
            return

        if len(name) < 2:
            messagebox.showwarning("Validation Error", "Please enter a valid student name.")
            return

        # Email Regex check
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            messagebox.showwarning("Validation Error", "Please enter a valid email address (e.g. name@domain.com).")
            return

        # Phone digits check
        clean_phone = re.sub(r"\D", "", phone)
        if len(clean_phone) != 10:
            messagebox.showwarning("Validation Error", "Please enter a valid 10-digit mobile number.")
            return

        try:
            self.controller.db.add_student(roll, name, course, email, clean_phone)
            self.feedback_lbl.config(
                text=f"✓ Success: Student '{name}' (Roll No: {roll}) saved successfully!",
                fg=THEME["success"]
            )
            messagebox.showinfo("Student Saved", f"Student '{name}' registered successfully.")
            self.clear_fields()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate Roll Number", f"A student with Roll Number '{roll}' already exists in the database.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while saving: {str(e)}")


# ==============================================================================
# 3. VIEW STUDENTS PAGE
# ==============================================================================
class ViewStudentsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Header toolbar
        header = tk.Frame(card, bg="#ffffff", padx=20, pady=16)
        header.pack(fill=tk.X)

        title_box = tk.Frame(header, bg="#ffffff")
        title_box.pack(side=tk.LEFT)

        tk.Label(
            title_box,
            text="All Student Records",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg=THEME["text_dark"]
        ).pack(anchor="w")

        self.count_badge = tk.Label(
            title_box,
            text="Total: 0 records",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_muted"]
        )
        self.count_badge.pack(anchor="w")

        # Action Buttons in toolbar
        btn_toolbar = tk.Frame(header, bg="#ffffff")
        btn_toolbar.pack(side=tk.RIGHT)

        btn_export = tk.Button(
            btn_toolbar,
            text="📥 Export CSV",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.export_csv
        )
        btn_export.pack(side=tk.LEFT, padx=4)

        btn_refresh = tk.Button(
            btn_toolbar,
            text="🔄 Refresh",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.load_records
        )
        btn_refresh.pack(side=tk.LEFT, padx=4)

        btn_edit = tk.Button(
            btn_toolbar,
            text="✏️ Edit Selected",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.edit_selected
        )
        btn_edit.pack(side=tk.LEFT, padx=4)

        btn_del = tk.Button(
            btn_toolbar,
            text="🗑️ Delete Selected",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["danger"],
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.delete_selected
        )
        btn_del.pack(side=tk.LEFT, padx=4)

        # Table & Scrollbar Container
        table_container = tk.Frame(card, bg="#ffffff")
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        cols = ("id", "roll", "name", "course", "email", "phone", "created_at")
        self.tree = ttk.Treeview(
            table_container,
            columns=cols,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("roll", text="Roll No")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("course", text="Course / Department")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone Number")
        self.tree.heading("created_at", text="Registered At")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("roll", width=100, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("course", width=190, anchor="w")
        self.tree.column("email", width=200, anchor="w")
        self.tree.column("phone", width=130, anchor="center")
        self.tree.column("created_at", width=150, anchor="center")

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        # Double click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_selected())

    def on_show(self):
        self.load_records()

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.controller.db.get_all_students()
        for idx, row in enumerate(records):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", tk.END, values=row, tags=(tag,))

        self.tree.tag_configure("even", background="#ffffff")
        self.tree.tag_configure("odd", background="#f8fafc")
        self.count_badge.config(text=f"Total: {len(records)} students registered in database")

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a student from the table to edit.")
            return
        values = self.tree.item(selected[0], "values")
        student_id = int(values[0])
        self.controller.navigate_to_update(student_id)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a student from the table to delete.")
            return
        values = self.tree.item(selected[0], "values")
        student_id = int(values[0])
        self.controller.navigate_to_delete(student_id)

    def export_csv(self):
        records = self.controller.db.get_all_students()
        if not records:
            messagebox.showwarning("No Data", "There are no student records to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Student Records CSV"
        )
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Roll Number", "Full Name", "Course", "Email", "Phone", "Registration Date"])
                writer.writerows(records)
            messagebox.showinfo("Export Successful", f"Records successfully exported to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not write CSV file: {str(e)}")


# ==============================================================================
# 4. UPDATE STUDENT PAGE
# ==============================================================================
class UpdateStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.current_student_id = None
        self.build_ui()

    def build_ui(self):
        card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(card, bg="#ffffff", padx=24, pady=18)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Update Existing Student Information",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg=THEME["text_dark"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Search student by Roll Number or pick from the dropdown to load and edit details.",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_muted"]
        ).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(card, bg=THEME["card_border"], height=1)
        sep.pack(fill=tk.X)

        # Search Bar to Select Student
        lookup_bar = tk.Frame(card, bg="#f8fafc", padx=24, pady=12, highlightbackground=THEME["card_border"], highlightthickness=1)
        lookup_bar.pack(fill=tk.X, padx=24, pady=14)

        tk.Label(
            lookup_bar,
            text="Quick Lookup by Roll No:",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc",
            fg=THEME["text_dark"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.lookup_entry = tk.Entry(lookup_bar, font=("Segoe UI", 10), width=18, bd=1, relief="solid")
        self.lookup_entry.pack(side=tk.LEFT, padx=(0, 8), ipady=3)
        self.lookup_entry.bind("<Return>", lambda e: self.search_and_load())

        btn_find = tk.Button(
            lookup_bar,
            text="🔍 Find & Load",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.search_and_load
        )
        btn_find.pack(side=tk.LEFT, padx=(0, 16))

        tk.Label(
            lookup_bar,
            text="Or Pick Student:",
            font=("Segoe UI", 9),
            bg="#f8fafc",
            fg=THEME["text_muted"]
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.combo_students = ttk.Combobox(lookup_bar, font=("Segoe UI", 9), state="readonly", width=34)
        self.combo_students.pack(side=tk.LEFT, ipady=2)
        self.combo_students.bind("<<ComboboxSelected>>", self.on_student_picked)

        # Form Edit Area
        form_frame = tk.Frame(card, bg="#ffffff", padx=30, pady=16)
        form_frame.pack(fill=tk.BOTH, expand=True)

        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

        # Editing indicator badge
        self.status_badge = tk.Label(
            form_frame,
            text="Status: No student selected. Please load a record to edit.",
            font=("Segoe UI", 9, "bold"),
            bg="#fef3c7",
            fg="#92400e",
            padx=10,
            pady=6
        )
        self.status_badge.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 14))

        # Fields
        self.edit_name = self.create_form_field(form_frame, row=1, col=0, label="Full Name *")
        self.edit_roll = self.create_form_field(form_frame, row=1, col=1, label="Roll Number * (Unique)")

        # Course Combobox
        course_frame = tk.Frame(form_frame, bg="#ffffff")
        course_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(course_frame, text="Course / Department *", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(0, 5))
        self.edit_course = ttk.Combobox(
            course_frame,
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
        self.edit_course.pack(fill=tk.X, ipady=4)

        self.edit_email = self.create_form_field(form_frame, row=2, col=1, label="Email Address *")
        self.edit_phone = self.create_form_field(form_frame, row=3, col=0, label="Phone Number * (10 Digits)")

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_frame.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=20)

        self.btn_update = tk.Button(
            btn_frame,
            text="💾  Apply Changes & Update",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.apply_update
        )
        self.btn_update.pack(side=tk.LEFT, padx=(0, 12))

        btn_cancel = tk.Button(
            btn_frame,
            text="🔄  Reset",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.reset_form
        )
        btn_cancel.pack(side=tk.LEFT, padx=(0, 12))

        btn_nav_view = tk.Button(
            btn_frame,
            text="📋  Back to View Table",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=THEME["primary"],
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
            command=lambda: self.controller.show_page("View Students")
        )
        btn_nav_view.pack(side=tk.LEFT)

    def create_form_field(self, parent, row, col, label):
        f = tk.Frame(parent, bg="#ffffff")
        f.grid(row=row, column=col, sticky="ew", padx=10, pady=10)

        lbl = tk.Label(f, text=label, font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"])
        lbl.pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(f, font=("Segoe UI", 10), bd=1, relief="solid", highlightthickness=1, highlightcolor=THEME["primary"])
        entry.pack(fill=tk.X, ipady=5)
        return entry

    def on_show(self):
        self.refresh_student_dropdown()

    def refresh_student_dropdown(self):
        records = self.controller.db.get_all_students()
        options = [f"{r[1]} - {r[2]} ({r[3]})" for r in records]
        self.combo_students["values"] = options
        self.student_records_cache = records

    def on_student_picked(self, event=None):
        idx = self.combo_students.current()
        if idx >= 0 and idx < len(self.student_records_cache):
            record = self.student_records_cache[idx]
            self.populate_fields(record)

    def search_and_load(self):
        roll = self.lookup_entry.get().strip()
        if not roll:
            messagebox.showwarning("Input Required", "Please enter a roll number to search.")
            return

        record = self.controller.db.get_student_by_roll(roll)
        if not record:
            messagebox.showerror("Not Found", f"No student found with Roll Number '{roll}'.")
            return

        self.populate_fields(record)

    def load_student_by_id(self, student_id):
        record = self.controller.db.get_student_by_id(student_id)
        if record:
            self.populate_fields(record)

    def populate_fields(self, record):
        # record: (id, roll_no, name, course, email, phone, created_at)
        self.current_student_id = record[0]
        self.edit_roll.delete(0, tk.END)
        self.edit_roll.insert(0, record[1])

        self.edit_name.delete(0, tk.END)
        self.edit_name.insert(0, record[2])

        self.edit_course.set(record[3])

        self.edit_email.delete(0, tk.END)
        self.edit_email.insert(0, record[4])

        self.edit_phone.delete(0, tk.END)
        self.edit_phone.insert(0, record[5])

        self.status_badge.config(
            text=f"Editing: {record[2]} | Roll: {record[1]} (Database ID: {record[0]})",
            bg="#dbeafe",
            fg="#1e40af"
        )

    def reset_form(self):
        if self.current_student_id:
            self.load_student_by_id(self.current_student_id)
        else:
            self.edit_roll.delete(0, tk.END)
            self.edit_name.delete(0, tk.END)
            self.edit_email.delete(0, tk.END)
            self.edit_phone.delete(0, tk.END)
            self.status_badge.config(
                text="Status: Form reset. Please select a student.",
                bg="#fef3c7",
                fg="#92400e"
            )

    def apply_update(self):
        if not self.current_student_id:
            messagebox.showwarning("No Record Selected", "Please load a student record first before updating.")
            return

        name = self.edit_name.get().strip()
        roll = self.edit_roll.get().strip()
        course = self.edit_course.get().strip()
        email = self.edit_email.get().strip()
        phone = self.edit_phone.get().strip()

        if not all([name, roll, course, email, phone]):
            messagebox.showwarning("Incomplete Form", "All fields are required.")
            return

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            messagebox.showwarning("Validation Error", "Please provide a valid email format.")
            return

        clean_phone = re.sub(r"\D", "", phone)
        if len(clean_phone) != 10:
            messagebox.showwarning("Validation Error", "Please provide a valid 10-digit phone number.")
            return

        try:
            self.controller.db.update_student(self.current_student_id, roll, name, course, email, clean_phone)
            self.status_badge.config(
                text=f"✓ Updated successfully: {name} (Roll: {roll})",
                bg="#ecfdf5",
                fg="#065f46"
            )
            messagebox.showinfo("Update Complete", f"Student '{name}' has been updated successfully!")
            self.refresh_student_dropdown()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate Roll Number", f"Roll Number '{roll}' belongs to another student.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update record: {str(e)}")


# ==============================================================================
# 5. DELETE STUDENT PAGE
# ==============================================================================
class DeleteStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.selected_student_id = None
        self.build_ui()

    def build_ui(self):
        card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(card, bg="#ffffff", padx=24, pady=18)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Delete Student Record",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg=THEME["danger"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Carefully select the record to remove. A confirmation prompt will safeguard against accidental deletion.",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_muted"]
        ).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(card, bg=THEME["card_border"], height=1)
        sep.pack(fill=tk.X)

        # Selection bar
        bar = tk.Frame(card, bg="#f8fafc", padx=24, pady=12, highlightbackground=THEME["card_border"], highlightthickness=1)
        bar.pack(fill=tk.X, padx=24, pady=14)

        tk.Label(
            bar,
            text="Select Student to Remove:",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc",
            fg=THEME["text_dark"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.combo_students = ttk.Combobox(bar, font=("Segoe UI", 9), state="readonly", width=40)
        self.combo_students.pack(side=tk.LEFT, padx=(0, 10), ipady=3)
        self.combo_students.bind("<<ComboboxSelected>>", self.on_student_picked)

        btn_load = tk.Button(
            bar,
            text="Load Details",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.on_student_picked
        )
        btn_load.pack(side=tk.LEFT)

        # Preview Details Card
        self.preview_card = tk.Frame(card, bg="#ffffff", padx=30, pady=20)
        self.preview_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            self.preview_card,
            text="Record Preview & Verification",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg=THEME["text_dark"]
        ).pack(anchor="w", pady=(0, 10))

        self.info_box = tk.Label(
            self.preview_card,
            text="No student selected.\nPlease select a student record above to inspect before deleting.",
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg=THEME["text_muted"],
            justify=tk.LEFT,
            padx=20,
            pady=20,
            relief="solid",
            bd=1
        )
        self.info_box.pack(fill=tk.X, pady=(0, 20))

        # Action Buttons
        btn_box = tk.Frame(self.preview_card, bg="#ffffff")
        btn_box.pack(anchor="w")

        self.btn_delete = tk.Button(
            btn_box,
            text="🗑️  Confirm & Delete Record",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["danger"],
            fg="#ffffff",
            relief="flat",
            padx=22,
            pady=9,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.confirm_and_delete
        )
        self.btn_delete.pack(side=tk.LEFT, padx=(0, 12))

        btn_cancel = tk.Button(
            btn_box,
            text="Cancel / Go Back",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=16,
            pady=9,
            cursor="hand2",
            command=lambda: self.controller.show_page("View Students")
        )
        btn_cancel.pack(side=tk.LEFT)

    def on_show(self):
        self.refresh_student_dropdown()

    def refresh_student_dropdown(self):
        records = self.controller.db.get_all_students()
        options = [f"{r[1]} - {r[2]} ({r[3]})" for r in records]
        self.combo_students["values"] = options
        self.student_records_cache = records

    def on_student_picked(self, event=None):
        idx = self.combo_students.current()
        if idx >= 0 and idx < len(self.student_records_cache):
            record = self.student_records_cache[idx]
            self.load_student_details(record)

    def load_student_by_id(self, student_id):
        self.refresh_student_dropdown()
        record = self.controller.db.get_student_by_id(student_id)
        if record:
            self.load_student_details(record)
            # Find and set in combobox
            for idx, r in enumerate(self.student_records_cache):
                if r[0] == student_id:
                    self.combo_students.current(idx)
                    break

    def load_student_details(self, record):
        # record: (id, roll_no, name, course, email, phone, created_at)
        self.selected_student_id = record[0]
        self.current_record = record

        details_text = (
            f"  • Student ID:     {record[0]}\n"
            f"  • Roll Number:    {record[1]}\n"
            f"  • Full Name:      {record[2]}\n"
            f"  • Course/Dept:    {record[3]}\n"
            f"  • Email:          {record[4]}\n"
            f"  • Phone Number:   {record[5]}\n"
            f"  • Registered:     {record[6]}\n"
        )
        self.info_box.config(
            text=details_text,
            fg=THEME["text_dark"],
            bg="#fff1f2",
            font=("Segoe UI", 10)
        )
        self.btn_delete.config(state=tk.NORMAL)

    def confirm_and_delete(self):
        if not self.selected_student_id or not hasattr(self, "current_record"):
            return

        name = self.current_record[2]
        roll = self.current_record[1]

        answer = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete student:\n\n"
            f"Name: {name}\nRoll No: {roll}\n\nThis action cannot be undone!",
            icon="warning"
        )

        if answer:
            try:
                self.controller.db.delete_student(self.selected_student_id)
                messagebox.showinfo("Deleted", f"Record for '{name}' was deleted successfully.")
                self.selected_student_id = None
                self.info_box.config(
                    text="Record deleted. Select another record to delete or navigate to another page.",
                    fg=THEME["text_muted"],
                    bg="#f8fafc"
                )
                self.btn_delete.config(state=tk.DISABLED)
                self.refresh_student_dropdown()
                self.combo_students.set("")
            except Exception as e:
                messagebox.showerror("Deletion Error", f"Could not delete student: {str(e)}")


# ==============================================================================
# 6. SEARCH STUDENT PAGE
# ==============================================================================
class SearchStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(card, bg="#ffffff", padx=24, pady=16)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Search Student Records",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg=THEME["text_dark"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Query records in real-time by Name, Roll Number, Course, or across all attributes.",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_muted"]
        ).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(card, bg=THEME["card_border"], height=1)
        sep.pack(fill=tk.X)

        # Search Controls Area
        controls_frame = tk.Frame(card, bg="#f8fafc", padx=24, pady=16, highlightbackground=THEME["card_border"], highlightthickness=1)
        controls_frame.pack(fill=tk.X, padx=20, pady=14)

        # Top row: Input & Search button
        input_row = tk.Frame(controls_frame, bg="#f8fafc")
        input_row.pack(fill=tk.X)

        tk.Label(input_row, text="Search Query:", font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 10))

        self.search_entry = tk.Entry(input_row, font=("Segoe UI", 10), bd=1, relief="solid")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12), ipady=4)
        self.search_entry.bind("<KeyRelease>", lambda e: self.perform_search())

        btn_search = tk.Button(
            input_row,
            text="🔍 Search",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=16,
            pady=4,
            cursor="hand2",
            command=self.perform_search
        )
        btn_search.pack(side=tk.LEFT, padx=(0, 6))

        btn_clear = tk.Button(
            input_row,
            text="Reset",
            font=("Segoe UI", 9),
            bg="#e2e8f0",
            fg=THEME["text_dark"],
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.reset_search
        )
        btn_clear.pack(side=tk.LEFT)

        # Radio filter criteria
        filter_row = tk.Frame(controls_frame, bg="#f8fafc")
        filter_row.pack(fill=tk.X, pady=(10, 0))

        tk.Label(filter_row, text="Filter By:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg=THEME["text_muted"]).pack(side=tk.LEFT, padx=(0, 12))

        self.filter_var = tk.StringVar(value="all")
        filters = [("All Fields", "all"), ("Roll Number", "roll"), ("Name", "name"), ("Course", "course")]
        for text, val in filters:
            r = tk.Radiobutton(
                filter_row,
                text=text,
                variable=self.filter_var,
                value=val,
                bg="#f8fafc",
                font=("Segoe UI", 9),
                activebackground="#f8fafc",
                command=self.perform_search
            )
            r.pack(side=tk.LEFT, padx=8)

        # Results status bar
        self.results_badge = tk.Label(
            card,
            text="Showing all records",
            font=("Segoe UI", 9, "italic"),
            bg="#ffffff",
            fg=THEME["text_muted"],
            padx=24
        )
        self.results_badge.pack(anchor="w", pady=(0, 8))

        # Results Table
        table_container = tk.Frame(card, bg="#ffffff")
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        cols = ("id", "roll", "name", "course", "email", "phone")
        self.tree = ttk.Treeview(
            table_container,
            columns=cols,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("roll", text="Roll No")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("course", text="Course / Dept")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("roll", width=110, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("course", width=200, anchor="w")
        self.tree.column("email", width=220, anchor="w")
        self.tree.column("phone", width=140, anchor="center")

        scroll = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Context action buttons below search table
        action_bar = tk.Frame(card, bg="#ffffff", padx=20, pady=10)
        action_bar.pack(fill=tk.X)

        btn_edit_found = tk.Button(
            action_bar,
            text="✏️ Edit Selected Result",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.edit_selected_result
        )
        btn_edit_found.pack(side=tk.LEFT, padx=(0, 8))

        btn_del_found = tk.Button(
            action_bar,
            text="🗑️ Delete Selected Result",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["danger"],
            fg="#ffffff",
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.delete_selected_result
        )
        btn_del_found.pack(side=tk.LEFT)

    def on_show(self):
        self.perform_search()

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.filter_var.set("all")
        self.perform_search()

    def perform_search(self):
        query = self.search_entry.get().strip()
        criteria = self.filter_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not query:
            records = self.controller.db.get_all_students()
            self.results_badge.config(text=f"Displaying all {len(records)} records in database.")
        else:
            records = self.controller.db.search_students(query, field=criteria)
            self.results_badge.config(text=f"Found {len(records)} matching student(s) for query '{query}'.")

        for idx, r in enumerate(records):
            tag = "even" if idx % 2 == 0 else "odd"
            # r: id, roll, name, course, email, phone, created_at
            self.tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4], r[5]), tags=(tag,))

        self.tree.tag_configure("even", background="#ffffff")
        self.tree.tag_configure("odd", background="#f8fafc")

    def edit_selected_result(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Record", "Please select a record from the search results to edit.")
            return
        val = self.tree.item(sel[0], "values")
        self.controller.navigate_to_update(int(val[0]))

    def delete_selected_result(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Record", "Please select a record from the search results to delete.")
            return
        val = self.tree.item(sel[0], "values")
        self.controller.navigate_to_delete(int(val[0]))


# ==============================================================================
# 7. ABOUT PAGE
# ==============================================================================
class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        card = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(card, bg="#ffffff", padx=24, pady=18)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="About Project | Student Record Management System",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg=THEME["text_dark"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Program No. 28 - Complete Desktop CRUD Application with GUI and SQLite Integration.",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_muted"]
        ).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(card, bg=THEME["card_border"], height=1)
        sep.pack(fill=tk.X)

        # Content Box
        content_box = tk.Frame(card, bg="#ffffff", padx=30, pady=20)
        content_box.pack(fill=tk.BOTH, expand=True)

        # Project Details Card
        proj_card = tk.LabelFrame(
            content_box,
            text=" 🎯 Practical AIM & Scope ",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg=THEME["primary"],
            padx=16,
            pady=12
        )
        proj_card.pack(fill=tk.X, pady=(0, 14))

        aim_text = (
            "Program No. 28\n"
            "AIM: To develop a complete desktop CRUD application (mini project with 6–7 pages/forms) "
            "integrating GUI, database and AI-assisted code generation.\n\n"
            "This project implements a multi-form Student Record Management System featuring:\n"
            "  1. Dashboard (KPI statistics, quick action shortcuts, recent registrations preview)\n"
            "  2. Add Student Form (Clean form inputs, email & phone validation, duplicate roll prevention)\n"
            "  3. View Students Table (Full interactive tabular display, striped rows, sorting, CSV export)\n"
            "  4. Update Student Form (Lookup by roll or selection, auto-population, in-place edit & save)\n"
            "  5. Delete Student Form (Protected deletion workflow with visual details card & modal confirmation)\n"
            "  6. Search Student System (Dynamic real-time multi-field search and query filtering)\n"
            "  7. About & Documentation (Tech stack summary, student credentials, and architecture specs)"
        )
        tk.Label(
            proj_card,
            text=aim_text,
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_dark"],
            justify=tk.LEFT
        ).pack(anchor="w")

        # Two-column layout for Developer Info and Tech Stack
        cols_frame = tk.Frame(content_box, bg="#ffffff")
        cols_frame.pack(fill=tk.X)
        cols_frame.columnconfigure(0, weight=1)
        cols_frame.columnconfigure(1, weight=1)

        # Tech Stack Box
        tech_card = tk.LabelFrame(
            cols_frame,
            text=" 🛠️ Technologies & Tools Used ",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg=THEME["primary"],
            padx=16,
            pady=12
        )
        tech_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tech_text = (
            "• Language:         Python 3.x\n"
            "• GUI Framework:    Tkinter & ttk\n"
            "• Database:         SQLite3 (Embedded Relational DB)\n"
            "• Architecture:     Object-Oriented Desktop App (OOP)\n"
            "• Styling Theme:    Modern Slate & Indigo Card Palette\n"
            "• High DPI:         Windows DPI Aware Rendering\n"
            "• AI Methodology:   AI-Assisted Pair Programming & Verification"
        )
        tk.Label(
            tech_card,
            text=tech_text,
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_dark"],
            justify=tk.LEFT
        ).pack(anchor="w")

        # Developer Info Box
        dev_card = tk.LabelFrame(
            cols_frame,
            text=" 👨‍💻 Developer & Practical Info ",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg=THEME["primary"],
            padx=16,
            pady=12
        )
        dev_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        dev_text = (
            "• Developer:        Darshan Mehta\n"
            "• Practical Course: Vibe Coding Practical Series\n"
            "• Practical Lab:    Program No. 28\n"
            "• Application:      Student Record Management System\n"
            "• Status:           Completed & Verified\n"
            "• Local Database:   student_records.db (Auto-managed)"
        )
        tk.Label(
            dev_card,
            text=dev_text,
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_dark"],
            justify=tk.LEFT
        ).pack(anchor="w")


def main():
    app = StudentManagementApp()
    app.mainloop()


if __name__ == "__main__":
    main()
