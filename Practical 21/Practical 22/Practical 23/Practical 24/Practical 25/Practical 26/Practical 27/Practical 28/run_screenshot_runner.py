"""
Practical 28 | Screenshot Runner Menu
Interactive launcher to open any of the 7 forms individually for taking screenshots.
"""

import sys
import subprocess
from pathlib import Path
import tkinter as tk

PAGES = [
    ("Page 1: Dashboard", "page1_dashboard.py", "👥 Metrics, KPI cards, recent registrations"),
    ("Page 2: Add Student", "page2_add_student.py", "➕ Registration form with validation"),
    ("Page 3: View Students", "page3_view_students.py", "📋 Treeview table, striped rows, CSV export"),
    ("Page 4: Update Student", "page4_update_student.py", "✏️  Student lookup, auto-fill, update form"),
    ("Page 5: Delete Student", "page5_delete_student.py", "🗑️  Record preview card & confirmation prompt"),
    ("Page 6: Search Student", "page6_search_student.py", "🔍 Real-time filter & search engine"),
    ("Page 7: About", "page7_about.py", "ℹ️  Aim, tech stack, and developer profile"),
]

BASE_DIR = Path(__file__).resolve().parent


class ScreenshotLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Practical 28 | Screenshot Helper Menu")
        self.geometry("680x580")
        self.configure(bg="#f8fafc")

        # Header
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=16)
        header.pack(fill=tk.X)
        tk.Label(header, text="Program No. 28 : Practical Screenshot Launcher", font=("Segoe UI", 13, "bold"), bg="#1e293b", fg="#ffffff").pack(anchor="w")
        tk.Label(header, text="Click any button below to launch that individual page for easy screenshot capture.", font=("Segoe UI", 9), bg="#1e293b", fg="#94a3b8").pack(anchor="w", pady=(2, 0))

        body = tk.Frame(self, bg="#f8fafc", padx=20, pady=16)
        body.pack(fill=tk.BOTH, expand=True)

        for title, filename, desc in PAGES:
            row = tk.Frame(body, bg="#ffffff", highlightbackground="#e2e8f0", highlightthickness=1, padx=14, pady=10)
            row.pack(fill=tk.X, pady=4)

            text_box = tk.Frame(row, bg="#ffffff")
            text_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(text_box, text=title, font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#0f172a").pack(anchor="w")
            tk.Label(text_box, text=desc, font=("Segoe UI", 8), bg="#ffffff", fg="#64748b").pack(anchor="w")

            btn = tk.Button(
                row,
                text="📷 Open for SS",
                font=("Segoe UI", 9, "bold"),
                bg="#4f46e5",
                fg="#ffffff",
                relief="flat",
                padx=12,
                pady=6,
                cursor="hand2",
                command=lambda f=filename: self.launch(f)
            )
            btn.pack(side=tk.RIGHT)

        # Center window
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def launch(self, filename):
        file_path = BASE_DIR / filename
        subprocess.Popen([sys.executable, str(file_path)], cwd=str(BASE_DIR))


if __name__ == "__main__":
    app = ScreenshotLauncher()
    app.mainloop()
