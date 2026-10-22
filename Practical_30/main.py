"""
Program No. 30: MAJOR PROJECT – II
Theme: Medical Store Billing System (PharmaCare POS & Inventory)
GUI: Tkinter + ttk (Multi-Screen Desktop Application with Menu Bar)
Database: SQLite3 (4 Normalized Tables)
Features: Full CRUD, POS Billing, Stock Control, File Handling (CSV/JSON/TXT), Reports
"""

import os
import sys
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Try enabling Windows high-DPI awareness
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

from database import DatabaseManager

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

# Color Palette (Medical Slate, Cyan & Emerald Theme)
THEME = {
    "sidebar_bg": "#0f172a",       # Deep Slate
    "sidebar_active": "#0284c7",   # Cyan Blue
    "sidebar_hover": "#1e293b",    # Slate Hover
    "header_bg": "#ffffff",        # Clean White
    "content_bg": "#f8fafc",       # Soft Grey
    "card_bg": "#ffffff",          # Pure White
    "card_border": "#e2e8f0",      # Border Grey
    "primary": "#0284c7",          # Medical Cyan
    "primary_hover": "#0369a1",
    "success": "#10b981",          # Emerald Green
    "warning": "#f59e0b",          # Amber
    "danger": "#ef4444",           # Crimson
    "text_dark": "#0f172a",        # Slate 900
    "text_muted": "#64748b",       # Slate 500
}


class PharmaCareApp(tk.Tk):
    """Main Application Window with Menu Bar and Multi-Screen Navigation."""

    def __init__(self):
        super().__init__()
        self.title("PharmaCare | Medical Store Billing & Inventory System (Program No. 30)")
        self.geometry("1180x740")
        self.minsize(1020, 660)
        self.configure(bg=THEME["content_bg"])

        # Initialize Database Manager
        self.db = DatabaseManager()

        # Configure TTK Styles
        self.setup_styles()

        # Build Menu Bar
        self.create_menu_bar()

        # Build Main Layout (Sidebar + Topbar + Content Container)
        self.create_main_layout()

        # Register and Build 5 Screens
        self.screens = {}
        self.create_screens()

        # Show initial screen (POS Billing)
        self.show_screen("POS Billing")

        # Center Window on Screen
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def setup_styles(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.style.configure(
            "Custom.Treeview",
            background="#ffffff",
            foreground=THEME["text_dark"],
            rowheight=30,
            fieldbackground="#ffffff",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            background="#f1f5f9",
            foreground=THEME["text_dark"],
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padding=(8, 8)
        )
        self.style.map(
            "Custom.Treeview",
            background=[("selected", THEME["primary"])],
            foreground=[("selected", "#ffffff")]
        )
        self.style.configure("Custom.TCombobox", padding=4, font=("Segoe UI", 9))

    def create_menu_bar(self):
        menubar = tk.Menu(self)

        # 1. File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="🧾 New Invoice / Billing (Ctrl+N)", command=lambda: self.show_screen("POS Billing"))
        file_menu.add_separator()
        file_menu.add_command(label="📥 Import Stock from CSV...", command=self.import_medicines_csv)
        file_menu.add_command(label="📤 Export Inventory to CSV...", command=self.export_medicines_csv)
        file_menu.add_command(label="📑 Export Sales to JSON...", command=self.export_invoices_json)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        # 2. Inventory Menu
        inv_menu = tk.Menu(menubar, tearoff=0)
        inv_menu.add_command(label="💊 Manage Medicines Catalog", command=lambda: self.show_screen("Medicine Inventory"))
        inv_menu.add_command(label="⚠️ View Low Stock Alerts", command=self.show_low_stock_dialog)
        menubar.add_cascade(label="Inventory", menu=inv_menu)

        # 3. Billing Menu
        bill_menu = tk.Menu(menubar, tearoff=0)
        bill_menu.add_command(label="🛒 POS Billing Terminal", command=lambda: self.show_screen("POS Billing"))
        bill_menu.add_command(label="📜 Sales & Invoice History", command=lambda: self.show_screen("Invoices History"))
        menubar.add_cascade(label="Billing", menu=bill_menu)

        # 4. Customers Menu
        cust_menu = tk.Menu(menubar, tearoff=0)
        cust_menu.add_command(label="👥 Customer Directory", command=lambda: self.show_screen("Customers"))
        menubar.add_cascade(label="Customers", menu=cust_menu)

        # 5. Reports Menu
        rep_menu = tk.Menu(menubar, tearoff=0)
        rep_menu.add_command(label="📊 Sales & Inventory Analytics", command=lambda: self.show_screen("Reports"))
        menubar.add_cascade(label="Reports", menu=rep_menu)

        # 6. Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="ℹ️ About PharmaCare", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def create_main_layout(self):
        # Left Sidebar Frame
        self.sidebar = tk.Frame(self, bg=THEME["sidebar_bg"], width=230)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Brand Logo Header
        brand_frame = tk.Frame(self.sidebar, bg=THEME["sidebar_bg"], padx=18, pady=20)
        brand_frame.pack(fill=tk.X)

        logo = tk.Label(brand_frame, text="💊", font=("Segoe UI", 18), bg=THEME["sidebar_bg"])
        logo.pack(side=tk.LEFT, padx=(0, 8))

        brand_text = tk.Frame(brand_frame, bg=THEME["sidebar_bg"])
        brand_text.pack(side=tk.LEFT)

        tk.Label(brand_text, text="PharmaCare", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg=THEME["sidebar_bg"]).pack(anchor="w")
        tk.Label(brand_text, text="Medical POS & Billing", font=("Segoe UI", 8), fg="#94a3b8", bg=THEME["sidebar_bg"]).pack(anchor="w")

        # Sidebar Separator
        tk.Frame(self.sidebar, bg="#1e293b", height=1).pack(fill=tk.X, padx=14, pady=(0, 14))

        # Nav items
        self.nav_items = [
            ("POS Billing", "  🛒   POS Billing"),
            ("Medicine Inventory", "  💊   Medicine Inventory"),
            ("Customers", "  👥   Customer Directory"),
            ("Invoices History", "  📜   Invoices & Sales"),
            ("Reports", "  📊   Reports & Analytics"),
        ]

        self.nav_buttons = {}
        for key, text in self.nav_items:
            btn = tk.Button(
                self.sidebar,
                text=text,
                font=("Segoe UI", 10),
                anchor="w",
                bg=THEME["sidebar_bg"],
                fg="#e2e8f0",
                activebackground=THEME["sidebar_hover"],
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                padx=18,
                pady=10,
                cursor="hand2",
                command=lambda k=key: self.show_screen(k)
            )
            btn.pack(fill=tk.X, pady=1)
            self.nav_buttons[key] = btn

        # Sidebar Footer
        footer = tk.Frame(self.sidebar, bg=THEME["sidebar_bg"], padx=16, pady=16)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(footer, text="Major Project – II\nProgram No. 30 • SQLite", font=("Segoe UI", 8), fg="#64748b", bg=THEME["sidebar_bg"], justify=tk.LEFT).pack(anchor="w")

        # Right Master Container
        self.right_container = tk.Frame(self, bg=THEME["content_bg"])
        self.right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Top Bar
        top_bar = tk.Frame(self.right_container, bg=THEME["header_bg"], height=56, padx=24)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        top_bar.pack_propagate(False)

        self.screen_title = tk.Label(top_bar, text="POS Billing Terminal", font=("Segoe UI", 14, "bold"), bg=THEME["header_bg"], fg=THEME["text_dark"])
        self.screen_title.pack(side=tk.LEFT, pady=14)

        status_pill = tk.Label(top_bar, text="● SQLite Database Active", font=("Segoe UI", 9, "bold"), bg="#ecfdf5", fg="#059669", padx=10, pady=3)
        status_pill.pack(side=tk.RIGHT, pady=15)

        tk.Frame(self.right_container, bg=THEME["card_border"], height=1).pack(side=tk.TOP, fill=tk.X)

        # Content Dynamic Area
        self.content_area = tk.Frame(self.right_container, bg=THEME["content_bg"], padx=20, pady=16)
        self.content_area.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def create_screens(self):
        from screen1_billing import BillingScreen
        from screen2_inventory import InventoryScreen
        from screen3_customers import CustomersScreen
        from screen4_invoices import InvoicesScreen
        from screen5_reports import ReportsScreen

        self.screens["POS Billing"] = BillingScreen(self.content_area, self)
        self.screens["Medicine Inventory"] = InventoryScreen(self.content_area, self)
        self.screens["Customers"] = CustomersScreen(self.content_area, self)
        self.screens["Invoices History"] = InvoicesScreen(self.content_area, self)
        self.screens["Reports"] = ReportsScreen(self.content_area, self)

        for s in self.screens.values():
            s.grid(row=0, column=0, sticky="nsew")

        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

    def show_screen(self, screen_name):
        screen = self.screens.get(screen_name)
        if not screen:
            return

        screen.tkraise()
        if hasattr(screen, "on_show"):
            screen.on_show()

        self.screen_title.config(text=screen_name)

        for key, btn in self.nav_buttons.items():
            if key == screen_name:
                btn.config(bg=THEME["sidebar_active"], fg="#ffffff", font=("Segoe UI", 10, "bold"))
            else:
                btn.config(bg=THEME["sidebar_bg"], fg="#e2e8f0", font=("Segoe UI", 10))

    # File Menu Actions
    def export_medicines_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="medicines_inventory.csv",
            title="Export Medicines Inventory CSV"
        )
        if file_path:
            count = self.db.export_medicines_csv(file_path)
            messagebox.showinfo("Export Successful", f"Successfully exported {count} medicine records to:\n{file_path}")

    def import_medicines_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Import Medicines Stock CSV"
        )
        if file_path:
            try:
                count = self.db.import_medicines_csv(file_path)
                messagebox.showinfo("Import Successful", f"Successfully imported/updated {count} medicine records into database!")
                if "Medicine Inventory" in self.screens:
                    self.screens["Medicine Inventory"].on_show()
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import CSV: {str(e)}")

    def export_invoices_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="invoices_history.json",
            title="Export Sales Invoices JSON"
        )
        if file_path:
            count = self.db.export_invoices_json(file_path)
            messagebox.showinfo("Export Successful", f"Successfully exported {count} sales transactions to JSON:\n{file_path}")

    def show_low_stock_dialog(self):
        low_items = self.db.get_low_stock_medicines(threshold=10)
        msg = f"Found {len(low_items)} medicine(s) with stock <= 10 units:\n\n"
        for item in low_items:
            msg += f" • {item[2]} (Batch: {item[1]}) — Stock: {item[6]} units\n"
        messagebox.showwarning("Low Stock Alert", msg)

    def show_about_dialog(self):
        messagebox.showinfo(
            "About PharmaCare",
            "PharmaCare - Medical Store Billing System\n"
            "Program No. 30 : MAJOR PROJECT – II\n\n"
            "• GUI Framework: Tkinter & ttk (Python 3.x)\n"
            "• Database: SQLite3 (4 Normalized Relational Tables)\n"
            "• Features: POS Terminal, Cart Calculation, Stock Control, CSV/JSON I/O, Reports\n"
            "• Developer: Darshan Mehta\n"
            "• Distributable: PyInstaller Executable Ready"
        )


def main():
    app = PharmaCareApp()
    app.mainloop()


if __name__ == "__main__":
    main()
