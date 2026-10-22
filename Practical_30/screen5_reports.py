"""
Practical 30 | Screen 5: Reports & Business Analytics
Can be imported into main.py or run standalone for taking practical screenshots.
Features:
- Live KPI Metrics (Total Revenue, Invoices, Medicines, Stock Count, Low Stock Alerts)
- Category Sales & Revenue Breakdown Table
- Low Stock Re-order Alert Table
- Refresh & CSV Export capabilities
"""

import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from database import DatabaseManager

BASE_DIR = Path(__file__).resolve().parent

THEME = {
    "header_bg": "#0f172a",
    "content_bg": "#f8fafc",
    "card_bg": "#ffffff",
    "card_border": "#e2e8f0",
    "primary": "#0284c7",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "text_dark": "#0f172a",
    "text_muted": "#64748b",
}


class ReportsScreen(tk.Frame):
    """Reports and Business Analytics Dashboard."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.db = controller.db if controller else DatabaseManager()

        self.build_ui()
        self.refresh_all_data()

    def build_ui(self):
        main_box = tk.Frame(self, bg=THEME["content_bg"])
        main_box.pack(fill=tk.BOTH, expand=True)

        # ------------------ KPI STAT CARDS ROW ------------------
        kpi_row = tk.Frame(main_box, bg=THEME["content_bg"])
        kpi_row.pack(fill=tk.X, pady=(0, 14))

        # We'll create 5 metric cards: Revenue, Invoices, Medicines, Total Stock, Low Stock
        self.lbl_stat_revenue = self.create_kpi_card(kpi_row, "Total Sales Revenue", "₹0.00", "#059669", "#ecfdf5")
        self.lbl_stat_invoices = self.create_kpi_card(kpi_row, "Invoices Issued", "0", "#2563eb", "#eff6ff")
        self.lbl_stat_meds = self.create_kpi_card(kpi_row, "Medicines Catalog", "0", "#7c3aed", "#f5f3ff")
        self.lbl_stat_stock = self.create_kpi_card(kpi_row, "Total Inventory Units", "0", "#0284c7", "#f0f9ff")
        self.lbl_stat_low = self.create_kpi_card(kpi_row, "Low Stock Warnings", "0", "#dc2626", "#fef2f2")

        # ------------------ TOOLBAR & REFRESH ------------------
        toolbar = tk.Frame(main_box, bg="#ffffff", padx=14, pady=8, highlightbackground=THEME["card_border"], highlightthickness=1)
        toolbar.pack(fill=tk.X, pady=(0, 12))

        tk.Label(toolbar, text="📊 Real-Time Summarized Reports", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT)

        btn_refresh = tk.Button(
            toolbar,
            text="🔄 Refresh Analytics",
            font=("Segoe UI", 9, "bold"),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.refresh_all_data
        )
        btn_refresh.pack(side=tk.RIGHT)

        btn_export_category = tk.Button(
            toolbar,
            text="📤 Export Category Report (CSV)",
            font=("Segoe UI", 8, "bold"),
            bg="#ecfdf5",
            fg="#059669",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.export_category_report_csv
        )
        btn_export_category.pack(side=tk.RIGHT, padx=6)

        # ------------------ SPLIT REPORTS NOTEBOOK / TABS ------------------
        notebook = ttk.Notebook(main_box)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Category Sales & Revenue Breakdown
        tab1 = tk.Frame(notebook, bg="#ffffff", padx=12, pady=12)
        notebook.add(tab1, text="  📈 Category Performance & Revenue  ")

        cols_tab1 = ("category", "titles", "stock_units", "units_sold", "revenue")
        self.tree_cats = ttk.Treeview(
            tab1,
            columns=cols_tab1,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )
        self.tree_cats.heading("category", text="Medicine Category")
        self.tree_cats.heading("titles", text="Unique Products")
        self.tree_cats.heading("stock_units", text="In-Stock Units")
        self.tree_cats.heading("units_sold", text="Units Dispensed")
        self.tree_cats.heading("revenue", text="Gross Revenue (₹)")

        self.tree_cats.column("category", width=180, anchor="w")
        self.tree_cats.column("titles", width=120, anchor="center")
        self.tree_cats.column("stock_units", width=120, anchor="center")
        self.tree_cats.column("units_sold", width=120, anchor="center")
        self.tree_cats.column("revenue", width=140, anchor="e")

        scroll_c_y = ttk.Scrollbar(tab1, orient=tk.VERTICAL, command=self.tree_cats.yview)
        self.tree_cats.configure(yscrollcommand=scroll_c_y.set)
        self.tree_cats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_c_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Tab 2: Low Stock Re-order Alert
        tab2 = tk.Frame(notebook, bg="#ffffff", padx=12, pady=12)
        notebook.add(tab2, text="  ⚠️ Low Stock & Re-order Alerts  ")

        cols_tab2 = ("id", "batch", "name", "category", "mfg", "price", "stock", "expiry")
        self.tree_low = ttk.Treeview(
            tab2,
            columns=cols_tab2,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )
        self.tree_low.heading("id", text="ID")
        self.tree_low.heading("batch", text="Batch #")
        self.tree_low.heading("name", text="Medicine Name")
        self.tree_low.heading("category", text="Category")
        self.tree_low.heading("mfg", text="Manufacturer")
        self.tree_low.heading("price", text="Price (₹)")
        self.tree_low.heading("stock", text="Remaining Stock")
        self.tree_low.heading("expiry", text="Expiry Date")

        self.tree_low.column("id", width=40, anchor="center")
        self.tree_low.column("batch", width=90, anchor="center")
        self.tree_low.column("name", width=170, anchor="w")
        self.tree_low.column("category", width=120, anchor="w")
        self.tree_low.column("mfg", width=130, anchor="w")
        self.tree_low.column("price", width=80, anchor="e")
        self.tree_low.column("stock", width=100, anchor="center")
        self.tree_low.column("expiry", width=90, anchor="center")

        scroll_l_y = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=self.tree_low.yview)
        self.tree_low.configure(yscrollcommand=scroll_l_y.set)
        self.tree_low.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_l_y.pack(side=tk.RIGHT, fill=tk.Y)

    def create_kpi_card(self, parent, title, initial_val, text_color, bg_color):
        card = tk.Frame(
            parent,
            bg="#ffffff",
            padx=14,
            pady=12,
            highlightbackground=THEME["card_border"],
            highlightthickness=1
        )
        card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), fg=THEME["text_muted"], bg="#ffffff").pack(anchor="w")
        lbl_val = tk.Label(card, text=initial_val, font=("Segoe UI", 15, "bold"), fg=text_color, bg="#ffffff")
        lbl_val.pack(anchor="w", pady=(4, 0))
        return lbl_val

    def refresh_all_data(self):
        # 1. Update KPI Cards
        kpi = self.db.get_kpi_metrics()
        self.lbl_stat_revenue.config(text=f"₹{kpi['total_revenue']:,.2f}")
        self.lbl_stat_invoices.config(text=str(kpi["total_invoices"]))
        self.lbl_stat_meds.config(text=str(kpi["total_meds"]))
        self.lbl_stat_stock.config(text=f"{kpi['total_stock']} units")
        self.lbl_stat_low.config(text=f"{kpi['low_stock']} items")

        # 2. Update Category Report Table
        for item in self.tree_cats.get_children():
            self.tree_cats.delete(item)

        cat_data = self.db.get_category_sales_breakdown()
        for row in cat_data:
            # (category, title_count, total_units, units_sold, revenue)
            cat = row[0]
            titles = row[1]
            stock = row[2]
            sold = row[3]
            rev = f"₹{row[4]:.2f}"
            self.tree_cats.insert("", tk.END, values=(cat, titles, stock, sold, rev))

        # 3. Update Low Stock Table
        for item in self.tree_low.get_children():
            self.tree_low.delete(item)

        low_data = self.db.get_low_stock_medicines(threshold=10)
        for r in low_data:
            # (id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date)
            med_id = r[0]
            batch = r[1]
            name = r[2]
            cat = r[3]
            mfg = r[4]
            price = f"₹{r[5]:.2f}"
            stock = f"⚠️ {r[6]} units"
            exp = r[7]
            self.tree_low.insert("", tk.END, values=(med_id, batch, name, cat, mfg, price, stock, exp))

    def export_category_report_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="category_sales_report.csv",
            title="Export Category Sales Report"
        )
        if not file_path:
            return

        cat_data = self.db.get_category_sales_breakdown()
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Unique Products", "In-Stock Units", "Units Sold", "Total Revenue (INR)"])
            for row in cat_data:
                writer.writerow(row)

        messagebox.showinfo("Export Successful", f"✓ Category report exported successfully to:\n{file_path}")

    def on_show(self):
        self.refresh_all_data()


class StandaloneReportsApp(tk.Tk):
    """Standalone runner for Screenshot capture."""
    def __init__(self):
        super().__init__()
        self.title("Screen 5: Reports & Analytics | PharmaCare Medical Store")
        self.geometry("1100x680")
        self.configure(bg=THEME["content_bg"])

        banner = tk.Frame(self, bg=THEME["header_bg"], height=52, padx=20)
        banner.pack(fill=tk.X)
        tk.Label(
            banner,
            text="PROGRAM 30 • SCREEN 5: REPORTS & BUSINESS ANALYTICS",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg=THEME["header_bg"]
        ).pack(side=tk.LEFT, pady=14)
        tk.Label(
            banner,
            text="● Summarized Aggregate Views",
            font=("Segoe UI", 9, "bold"),
            fg="#10b981",
            bg=THEME["header_bg"]
        ).pack(side=tk.RIGHT, pady=16)

        container = tk.Frame(self, bg=THEME["content_bg"], padx=18, pady=14)
        container.pack(fill=tk.BOTH, expand=True)

        screen = ReportsScreen(container)
        screen.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = StandaloneReportsApp()
    app.mainloop()
