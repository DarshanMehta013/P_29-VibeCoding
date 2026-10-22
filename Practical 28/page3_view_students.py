"""
Practical 28 | Form 3: View Students
Run this file standalone to view and screenshot the View Students table.
"""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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


class ViewStudentsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page 3: View Students | Student Record Management System")
        self.geometry("980x640")
        self.minsize(860, 560)
        self.configure(bg=THEME["content_bg"])

        self.db = DatabaseManager()
        self.setup_styles()
        self.create_layout()
        self.load_records()
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

        title = tk.Label(top_bar, text="  Form 3 of 7 : View Student Records Table", font=("Segoe UI", 13, "bold"), bg=THEME["header_bg"], fg="#ffffff")
        title.pack(side=tk.LEFT, pady=16)

        pill = tk.Label(top_bar, text="CRUD: READ / RETRIEVE", font=("Segoe UI", 9, "bold"), bg="#ecfdf5", fg="#059669", padx=10, pady=3)
        pill.pack(side=tk.RIGHT, pady=18)

        # Body Container
        body = tk.Frame(self, bg=THEME["content_bg"], padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(body, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Header toolbar
        header = tk.Frame(card, bg="#ffffff", padx=20, pady=16)
        header.pack(fill=tk.X)

        title_box = tk.Frame(header, bg="#ffffff")
        title_box.pack(side=tk.LEFT)

        tk.Label(title_box, text="All Registered Students", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w")
        self.count_badge = tk.Label(title_box, text="Loading records...", font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"])
        self.count_badge.pack(anchor="w")

        # Buttons on right
        btn_box = tk.Frame(header, bg="#ffffff")
        btn_box.pack(side=tk.RIGHT)

        btn_refresh = tk.Button(btn_box, text="🔄 Refresh Table", font=("Segoe UI", 9), bg="#f1f5f9", fg=THEME["text_dark"], relief="flat", padx=14, pady=6, cursor="hand2", command=self.load_records)
        btn_refresh.pack(side=tk.LEFT, padx=4)

        btn_export = tk.Button(btn_box, text="📥 Export CSV", font=("Segoe UI", 9, "bold"), bg=THEME["primary"], fg="#ffffff", relief="flat", padx=14, pady=6, cursor="hand2", command=self.export_csv)
        btn_export.pack(side=tk.LEFT, padx=4)

        # Table Container
        table_frame = tk.Frame(card, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        cols = ("id", "roll", "name", "course", "email", "phone", "created_at")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Custom.Treeview", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("roll", text="Roll No")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("course", text="Course / Department")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone Number")
        self.tree.heading("created_at", text="Registered On")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("roll", width=100, anchor="center")
        self.tree.column("name", width=190, anchor="w")
        self.tree.column("course", width=180, anchor="w")
        self.tree.column("email", width=190, anchor="w")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.column("created_at", width=140, anchor="center")

        y_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.db.get_all_students()
        for idx, row in enumerate(records):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", tk.END, values=row, tags=(tag,))

        self.tree.tag_configure("even", background="#ffffff")
        self.tree.tag_configure("odd", background="#f8fafc")
        self.count_badge.config(text=f"Total: {len(records)} student records stored in SQLite database.")

    def export_csv(self):
        records = self.db.get_all_students()
        if not records:
            messagebox.showwarning("No Data", "No records found to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Roll Number", "Full Name", "Course", "Email", "Phone", "Registration Date"])
                writer.writerows(records)
            messagebox.showinfo("Export Successful", f"Exported {len(records)} records to CSV!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = ViewStudentsWindow()
    app.mainloop()
