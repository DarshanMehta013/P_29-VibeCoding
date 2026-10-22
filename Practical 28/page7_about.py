"""
Practical 28 | Form 7: About
Run this file standalone to view and screenshot the About page.
"""

import tkinter as tk
from pathlib import Path

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


class AboutWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page 7: About Project | Student Record Management System")
        self.geometry("920x640")
        self.minsize(820, 560)
        self.configure(bg=THEME["content_bg"])

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

        title = tk.Label(top_bar, text="  Form 7 of 7 : About Project & Tech Stack", font=("Segoe UI", 13, "bold"), bg=THEME["header_bg"], fg="#ffffff")
        title.pack(side=tk.LEFT, pady=16)

        pill = tk.Label(top_bar, text="PROJECT METADATA", font=("Segoe UI", 9, "bold"), bg="#f3e8ff", fg="#7e22ce", padx=10, pady=3)
        pill.pack(side=tk.RIGHT, pady=18)

        # Body Container
        body = tk.Frame(self, bg=THEME["content_bg"], padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Header inside card
        header = tk.Frame(card, bg="#ffffff", padx=24, pady=18)
        header.pack(fill=tk.X)
        tk.Label(header, text="Student Record Management System v1.0", font=("Segoe UI", 15, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w")
        tk.Label(header, text="Desktop CRUD mini project integrating GUI, SQLite database, and AI-assisted workflow.", font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"]).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(card, bg=THEME["card_border"], height=1)
        sep.pack(fill=tk.X)

        content = tk.Frame(card, bg="#ffffff", padx=24, pady=18)
        content.pack(fill=tk.BOTH, expand=True)

        # Aim Section Box
        aim_box = tk.LabelFrame(content, text=" 🎯 Practical AIM & Scope ", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["primary"], padx=16, pady=12)
        aim_box.pack(fill=tk.X, pady=(0, 14))

        aim_desc = (
            "Program No. 28\n"
            "AIM: To develop a complete desktop CRUD application (mini project with 6–7 pages/forms) "
            "integrating GUI, database and AI-assisted code generation.\n\n"
            "Project Modules & 7 Forms Implemented:\n"
            "  • Form 1: Dashboard (Metrics, quick shortcuts, recent registrations table)\n"
            "  • Form 2: Add Student (Data validation, duplicate roll prevention, instant commit)\n"
            "  • Form 3: View Students (Custom-styled Treeview, column sorting, CSV export)\n"
            "  • Form 4: Update Student (Direct record loading, pre-population, in-place edit)\n"
            "  • Form 5: Delete Student (Safety verification card and modal confirmation dialog)\n"
            "  • Form 6: Search Student (Dynamic real-time search with multi-criteria filters)\n"
            "  • Form 7: About Page (System specifications, tech stack, and developer profile)"
        )
        tk.Label(aim_box, text=aim_desc, font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_dark"], justify=tk.LEFT).pack(anchor="w")

        # Two Column Grid for Tech Stack & Developer Profile
        cols = tk.Frame(content, bg="#ffffff")
        cols.pack(fill=tk.X)
        cols.columnconfigure(0, weight=1)
        cols.columnconfigure(1, weight=1)

        # Tech Stack Box
        tech_box = tk.LabelFrame(cols, text=" 🛠️ Technologies Used ", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["primary"], padx=16, pady=12)
        tech_box.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tech_text = (
            "• Language:         Python 3.x\n"
            "• GUI Toolkit:      Tkinter & ttk (Clam Style)\n"
            "• Database Engine:  SQLite3 (Embedded Relational DB)\n"
            "• Architecture:     Object-Oriented Programming (OOP)\n"
            "• UI Palette:       Modern Slate & Indigo Theme\n"
            "• Display Support:  Windows High-DPI Aware"
        )
        tk.Label(tech_box, text=tech_text, font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_dark"], justify=tk.LEFT).pack(anchor="w")

        # Developer Info Box
        dev_box = tk.LabelFrame(cols, text=" 👨‍💻 Developer & Lab Info ", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["primary"], padx=16, pady=12)
        dev_box.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        dev_text = (
            "• Student / Dev:    Darshan Mehta\n"
            "• Course:           Vibe Coding Practical Series\n"
            "• Practical Number: Program No. 28\n"
            "• Project Title:    Student Record Management System\n"
            "• Database File:    student_records.db\n"
            "• Lab Submission:   Screenshots Verified for Manual"
        )
        tk.Label(dev_box, text=dev_text, font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_dark"], justify=tk.LEFT).pack(anchor="w")


if __name__ == "__main__":
    app = AboutWindow()
    app.mainloop()
