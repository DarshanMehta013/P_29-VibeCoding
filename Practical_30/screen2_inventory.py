"""
Practical 30 | Screen 2: Medicine Inventory & Stock Management
Can be imported into main.py or run standalone for taking practical screenshots.
Features:
- Complete CRUD (Create, Read, Update, Delete)
- Form validation (types, required fields, numeric bounds)
- Confirmation dialogs before deletion
- Search filter & Category filter
- CSV Export and CSV Import
"""

import os
import datetime
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


class InventoryScreen(tk.Frame):
    """Medicine Inventory Management with CRUD, Search, and CSV Import/Export."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.db = controller.db if controller else DatabaseManager()

        self.selected_med_id = None
        self.build_ui()
        self.load_categories()
        self.load_inventory()

    def build_ui(self):
        # Top Container Split: Left (Input Form for Add/Edit) & Right (Catalog Table + Filters)
        main_box = tk.Frame(self, bg=THEME["content_bg"])
        main_box.pack(fill=tk.BOTH, expand=True)

        left_col = tk.Frame(main_box, bg=THEME["content_bg"], width=360)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 12))
        left_col.pack_propagate(False)

        right_col = tk.Frame(main_box, bg=THEME["content_bg"])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ------------------ LEFT COLUMN: FORM CARD ------------------
        form_card = tk.LabelFrame(
            left_col,
            text=" 📝 Medicine Details (Add / Edit) ",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg=THEME["primary"],
            padx=14,
            pady=12,
            highlightbackground=THEME["card_border"],
            highlightthickness=1,
            relief="flat"
        )
        form_card.pack(fill=tk.BOTH, expand=True)

        # Form Fields
        tk.Label(form_card, text="Batch No. *", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_batch = ttk.Entry(form_card, font=("Segoe UI", 9))
        self.entry_batch.pack(fill=tk.X, pady=(0, 8))

        tk.Label(form_card, text="Medicine Name *", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_name = ttk.Entry(form_card, font=("Segoe UI", 9))
        self.entry_name.pack(fill=tk.X, pady=(0, 8))

        tk.Label(form_card, text="Category *", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.combo_category = ttk.Combobox(
            form_card,
            values=["Antibiotic", "Analgesic", "Antacid", "Antihistamine", "Cardiology", "Supplements", "Antidiabetic", "Respiratory", "Topical"],
            font=("Segoe UI", 9)
        )
        self.combo_category.pack(fill=tk.X, pady=(0, 8))

        tk.Label(form_card, text="Manufacturer / Brand", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_mfg = ttk.Entry(form_card, font=("Segoe UI", 9))
        self.entry_mfg.pack(fill=tk.X, pady=(0, 8))

        # Price and Stock in single row
        row_ps = tk.Frame(form_card, bg="#ffffff")
        row_ps.pack(fill=tk.X, pady=(0, 8))

        p_frame = tk.Frame(row_ps, bg="#ffffff")
        p_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        tk.Label(p_frame, text="Unit Price (₹) *", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_price = ttk.Entry(p_frame, font=("Segoe UI", 9))
        self.entry_price.pack(fill=tk.X)

        s_frame = tk.Frame(row_ps, bg="#ffffff")
        s_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0))
        tk.Label(s_frame, text="Stock Qty *", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_stock = ttk.Entry(s_frame, font=("Segoe UI", 9))
        self.entry_stock.pack(fill=tk.X)

        tk.Label(form_card, text="Expiry Date (YYYY-MM-DD) *", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_expiry = ttk.Entry(form_card, font=("Segoe UI", 9))
        self.entry_expiry.pack(fill=tk.X, pady=(0, 14))

        # Form Buttons (CRUD Operations)
        btn_frame1 = tk.Frame(form_card, bg="#ffffff")
        btn_frame1.pack(fill=tk.X, pady=(0, 6))

        self.btn_save = tk.Button(
            btn_frame1,
            text="💾 Save New",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.save_medicine
        )
        self.btn_save.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_update = tk.Button(
            btn_frame1,
            text="✏️ Update",
            font=("Segoe UI", 9, "bold"),
            bg="#3b82f6",
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.update_medicine
        )
        self.btn_update.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        btn_frame2 = tk.Frame(form_card, bg="#ffffff")
        btn_frame2.pack(fill=tk.X, pady=(0, 10))

        self.btn_delete = tk.Button(
            btn_frame2,
            text="🗑️ Delete",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["danger"],
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.delete_medicine
        )
        self.btn_delete.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        btn_reset = tk.Button(
            btn_frame2,
            text="🔄 Clear Form",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.reset_form
        )
        btn_reset.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        # File Handling Actions Card inside Form
        tk.Frame(form_card, bg=THEME["card_border"], height=1).pack(fill=tk.X, pady=(8, 10))

        tk.Label(form_card, text="File Handling & Backup", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_muted"]).pack(anchor="w", pady=(0, 6))

        file_btn_frame = tk.Frame(form_card, bg="#ffffff")
        file_btn_frame.pack(fill=tk.X)

        btn_export_csv = tk.Button(
            file_btn_frame,
            text="📤 Export CSV",
            font=("Segoe UI", 8, "bold"),
            bg="#ecfdf5",
            fg="#059669",
            relief="flat",
            padx=8,
            pady=5,
            cursor="hand2",
            command=self.export_csv
        )
        btn_export_csv.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        btn_import_csv = tk.Button(
            file_btn_frame,
            text="📥 Import CSV",
            font=("Segoe UI", 8, "bold"),
            bg="#eff6ff",
            fg="#2563eb",
            relief="flat",
            padx=8,
            pady=5,
            cursor="hand2",
            command=self.import_csv
        )
        btn_import_csv.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        # ------------------ RIGHT COLUMN: SEARCH & TREEVIEW ------------------
        # Search & Filter Toolbar
        search_card = tk.Frame(right_col, bg="#ffffff", padx=14, pady=10, highlightbackground=THEME["card_border"], highlightthickness=1)
        search_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(search_card, text="🔍 Search:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 6))
        self.entry_search = ttk.Entry(search_card, font=("Segoe UI", 9), width=24)
        self.entry_search.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_search.bind("<KeyRelease>", lambda e: self.filter_medicines())

        tk.Label(search_card, text="Category:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 6))
        self.filter_category = ttk.Combobox(search_card, font=("Segoe UI", 9), state="readonly", width=16)
        self.filter_category.pack(side=tk.LEFT, padx=(0, 10))
        self.filter_category.bind("<<ComboboxSelected>>", lambda e: self.filter_medicines())

        btn_search_reset = tk.Button(
            search_card,
            text="Reset Filter",
            font=("Segoe UI", 8),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.reset_search
        )
        btn_search_reset.pack(side=tk.LEFT)

        self.lbl_record_count = tk.Label(search_card, text="Total: 0 medicines", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["primary"])
        self.lbl_record_count.pack(side=tk.RIGHT)

        # Treeview Table
        table_container = tk.Frame(right_col, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        table_container.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "batch", "name", "category", "manufacturer", "price", "stock", "expiry")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("batch", text="Batch #")
        self.tree.heading("name", text="Medicine Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("manufacturer", text="Manufacturer")
        self.tree.heading("price", text="Price (₹)")
        self.tree.heading("stock", text="Stock Qty")
        self.tree.heading("expiry", text="Expiry Date")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("batch", width=85, anchor="center")
        self.tree.column("name", width=160, anchor="w")
        self.tree.column("category", width=100, anchor="w")
        self.tree.column("manufacturer", width=110, anchor="w")
        self.tree.column("price", width=70, anchor="e")
        self.tree.column("stock", width=75, anchor="center")
        self.tree.column("expiry", width=85, anchor="center")

        scroll_y = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_categories(self):
        cats = self.db.get_categories()
        options = ["All"] + sorted(list(set(cats + ["Antibiotic", "Analgesic", "Antacid", "Antihistamine", "Cardiology", "Supplements"])))
        self.filter_category["values"] = options
        self.filter_category.set("All")

    def load_inventory(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if records is None:
            records = self.db.get_all_medicines()

        for r in records:
            # (id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at)
            med_id = r[0]
            batch = r[1]
            name = r[2]
            cat = r[3]
            mfg = r[4]
            price = f"₹{r[5]:.2f}"
            stock = r[6]
            expiry = r[7]

            self.tree.insert("", tk.END, values=(med_id, batch, name, cat, mfg, price, stock, expiry))

        self.lbl_record_count.config(text=f"Total: {len(records)} medicines")

    def filter_medicines(self):
        q = self.entry_search.get().strip()
        cat = self.filter_category.get()
        records = self.db.search_medicines(q, cat)
        self.load_inventory(records)

    def reset_search(self):
        self.entry_search.delete(0, tk.END)
        self.filter_category.set("All")
        self.load_inventory()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        if not values:
            return

        self.selected_med_id = int(values[0])
        med = self.db.get_medicine_by_id(self.selected_med_id)
        if not med:
            return

        # (id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at)
        self.reset_form_fields_only()
        self.entry_batch.insert(0, med[1])
        self.entry_name.insert(0, med[2])
        self.combo_category.set(med[3])
        self.entry_mfg.insert(0, med[4])
        self.entry_price.insert(0, str(med[5]))
        self.entry_stock.insert(0, str(med[6]))
        self.entry_expiry.insert(0, str(med[7]))

        self.btn_save.config(state=tk.DISABLED)
        self.btn_update.config(state=tk.NORMAL)
        self.btn_delete.config(state=tk.NORMAL)

    def validate_inputs(self):
        batch = self.entry_batch.get().strip()
        name = self.entry_name.get().strip()
        category = self.combo_category.get().strip()
        mfg = self.entry_mfg.get().strip()
        price_str = self.entry_price.get().strip()
        stock_str = self.entry_stock.get().strip()
        expiry = self.entry_expiry.get().strip()

        if not batch or not name or not category:
            messagebox.showwarning("Validation Error", "Batch Number, Medicine Name, and Category are required!")
            return None

        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Validation Error", "Price must be a valid positive number!")
            return None

        try:
            stock = int(stock_str)
            if stock < 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Validation Error", "Stock Quantity must be a valid non-negative whole integer!")
            return None

        if not expiry:
            messagebox.showwarning("Validation Error", "Expiry Date is required (e.g., 2027-12-31)!")
            return None

        return {
            "batch": batch,
            "name": name,
            "category": category,
            "mfg": mfg,
            "price": price,
            "stock": stock,
            "expiry": expiry
        }

    def save_medicine(self):
        data = self.validate_inputs()
        if not data:
            return

        try:
            new_id = self.db.add_medicine(
                batch_no=data["batch"],
                name=data["name"],
                category=data["category"],
                manufacturer=data["mfg"],
                price=data["price"],
                stock_qty=data["stock"],
                expiry_date=data["expiry"]
            )
            messagebox.showinfo("Success", f"✓ Medicine '{data['name']}' added successfully (ID: {new_id})!")
            self.reset_form()
            self.load_inventory()
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add medicine: {str(e)}")

    def update_medicine(self):
        if not self.selected_med_id:
            messagebox.showwarning("Warning", "Please select a medicine from the table to update.")
            return

        data = self.validate_inputs()
        if not data:
            return

        try:
            self.db.update_medicine(
                med_id=self.selected_med_id,
                batch_no=data["batch"],
                name=data["name"],
                category=data["category"],
                manufacturer=data["mfg"],
                price=data["price"],
                stock_qty=data["stock"],
                expiry_date=data["expiry"]
            )
            messagebox.showinfo("Success", f"✓ Medicine '{data['name']}' updated successfully!")
            self.reset_form()
            self.load_inventory()
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update medicine: {str(e)}")

    def delete_medicine(self):
        if not self.selected_med_id:
            messagebox.showwarning("Warning", "Please select a medicine from the table to delete.")
            return

        name = self.entry_name.get().strip() or f"ID {self.selected_med_id}"
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete medicine:\n\n'{name}'?\n\nThis action cannot be undone.",
            icon="warning"
        )
        if not confirm:
            return

        try:
            self.db.delete_medicine(self.selected_med_id)
            messagebox.showinfo("Deleted", f"✓ Medicine '{name}' has been deleted from inventory.")
            self.reset_form()
            self.load_inventory()
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete medicine: {str(e)}")

    def reset_form_fields_only(self):
        self.entry_batch.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.combo_category.set("")
        self.entry_mfg.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_expiry.delete(0, tk.END)

    def reset_form(self):
        self.selected_med_id = None
        self.reset_form_fields_only()
        self.btn_save.config(state=tk.NORMAL)
        self.btn_update.config(state=tk.DISABLED)
        self.btn_delete.config(state=tk.DISABLED)
        self.tree.selection_remove(self.tree.selection())

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="medicines_inventory.csv",
            title="Export Medicines Inventory CSV"
        )
        if file_path:
            count = self.db.export_medicines_csv(file_path)
            messagebox.showinfo("Export Successful", f"Successfully exported {count} medicine records to:\n{file_path}")

    def import_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Import Medicines Stock CSV"
        )
        if file_path:
            try:
                count = self.db.import_medicines_csv(file_path)
                messagebox.showinfo("Import Successful", f"Successfully imported/updated {count} medicine records into database!")
                self.load_inventory()
                self.load_categories()
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import CSV: {str(e)}")

    def on_show(self):
        """Called by main window when this screen is navigated to."""
        self.load_categories()
        self.load_inventory()


class StandaloneInventoryApp(tk.Tk):
    """Standalone runner for Screenshot capture."""
    def __init__(self):
        super().__init__()
        self.title("Screen 2: Medicine Inventory Management | PharmaCare Medical Store")
        self.geometry("1120x680")
        self.configure(bg=THEME["content_bg"])

        # Top Banner
        banner = tk.Frame(self, bg=THEME["header_bg"], height=52, padx=20)
        banner.pack(fill=tk.X)
        tk.Label(
            banner,
            text="PROGRAM 30 • SCREEN 2: MEDICINE INVENTORY & STOCK MANAGEMENT",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg=THEME["header_bg"]
        ).pack(side=tk.LEFT, pady=14)
        tk.Label(
            banner,
            text="● Complete CRUD & CSV I/O",
            font=("Segoe UI", 9, "bold"),
            fg="#10b981",
            bg=THEME["header_bg"]
        ).pack(side=tk.RIGHT, pady=16)

        container = tk.Frame(self, bg=THEME["content_bg"], padx=18, pady=14)
        container.pack(fill=tk.BOTH, expand=True)

        screen = InventoryScreen(container)
        screen.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = StandaloneInventoryApp()
    app.mainloop()
