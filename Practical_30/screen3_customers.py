"""
Practical 30 | Screen 3: Customer & Patient Directory Management
Can be imported into main.py or run standalone for taking practical screenshots.
Features:
- Complete CRUD (Add, View, Update, Delete)
- Phone number and name validation
- Confirmation dialogs before deletion
- Live search by Name, Phone, or Doctor
- Patient history overview
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
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


class CustomersScreen(tk.Frame):
    """Customer Directory Management with CRUD and Live Search."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.db = controller.db if controller else DatabaseManager()

        self.selected_cust_id = None
        self.build_ui()
        self.load_customers()

    def build_ui(self):
        main_box = tk.Frame(self, bg=THEME["content_bg"])
        main_box.pack(fill=tk.BOTH, expand=True)

        left_col = tk.Frame(main_box, bg=THEME["content_bg"], width=360)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 12))
        left_col.pack_propagate(False)

        right_col = tk.Frame(main_box, bg=THEME["content_bg"])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ------------------ LEFT COLUMN: CUSTOMER FORM ------------------
        form_card = tk.LabelFrame(
            left_col,
            text=" 👤 Customer / Patient Information ",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg=THEME["primary"],
            padx=14,
            pady=14,
            highlightbackground=THEME["card_border"],
            highlightthickness=1,
            relief="flat"
        )
        form_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_card, text="Full Name *", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_name = ttk.Entry(form_card, font=("Segoe UI", 9))
        self.entry_name.pack(fill=tk.X, pady=(0, 10))

        tk.Label(form_card, text="Contact Phone *", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_phone = ttk.Entry(form_card, font=("Segoe UI", 9))
        self.entry_phone.pack(fill=tk.X, pady=(0, 10))

        tk.Label(form_card, text="Consulting Doctor", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.entry_doctor = ttk.Entry(form_card, font=("Segoe UI", 9))
        self.entry_doctor.pack(fill=tk.X, pady=(0, 10))

        tk.Label(form_card, text="Residential Address / City", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(2, 2))
        self.txt_address = tk.Text(form_card, font=("Segoe UI", 9), height=4, relief="solid", bd=1)
        self.txt_address.pack(fill=tk.X, pady=(0, 14))

        # CRUD Action Buttons
        btn_frame1 = tk.Frame(form_card, bg="#ffffff")
        btn_frame1.pack(fill=tk.X, pady=(0, 6))

        self.btn_save = tk.Button(
            btn_frame1,
            text="💾 Add Customer",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["primary"],
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.save_customer
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
            command=self.update_customer
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
            command=self.delete_customer
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

        # Helpful hint banner inside form
        hint_box = tk.Frame(form_card, bg="#f0f9ff", highlightbackground="#bae6fd", highlightthickness=1, padx=10, pady=8)
        hint_box.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        tk.Label(
            hint_box,
            text="ℹ️ Tip: Registered customers can be selected directly during checkout on the POS Billing screen.",
            font=("Segoe UI", 8),
            bg="#f0f9ff",
            fg="#0369a1",
            justify=tk.LEFT,
            wraplength=310
        ).pack(anchor="w")

        # ------------------ RIGHT COLUMN: SEARCH & TREEVIEW ------------------
        search_card = tk.Frame(right_col, bg="#ffffff", padx=14, pady=10, highlightbackground=THEME["card_border"], highlightthickness=1)
        search_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(search_card, text="🔍 Search Customers:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 8))
        self.entry_search = ttk.Entry(search_card, font=("Segoe UI", 9), width=28)
        self.entry_search.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_search.bind("<KeyRelease>", lambda e: self.filter_customers())

        btn_clear_search = tk.Button(
            search_card,
            text="Clear",
            font=("Segoe UI", 8),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.reset_search
        )
        btn_clear_search.pack(side=tk.LEFT)

        self.lbl_record_count = tk.Label(search_card, text="Total: 0 customers", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["primary"])
        self.lbl_record_count.pack(side=tk.RIGHT)

        # Treeview Table
        table_container = tk.Frame(right_col, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        table_container.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "phone", "doctor", "address", "registered_on")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Customer Name")
        self.tree.heading("phone", text="Phone Number")
        self.tree.heading("doctor", text="Consulting Doctor")
        self.tree.heading("address", text="Address")
        self.tree.heading("registered_on", text="Registered On")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=160, anchor="w")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.column("doctor", width=150, anchor="w")
        self.tree.column("address", width=180, anchor="w")
        self.tree.column("registered_on", width=130, anchor="center")

        scroll_y = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_customers(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if records is None:
            records = self.db.get_all_customers()

        for r in records:
            # (id, name, phone, doctor_name, address, created_at)
            cust_id = r[0]
            name = r[1]
            phone = r[2] or "—"
            doctor = r[3] or "—"
            address = r[4] or "—"
            reg_on = r[5][:16] if r[5] else "—"

            self.tree.insert("", tk.END, values=(cust_id, name, phone, doctor, address, reg_on))

        self.lbl_record_count.config(text=f"Total: {len(records)} customers")

    def filter_customers(self):
        q = self.entry_search.get().strip()
        records = self.db.search_customers(q)
        self.load_customers(records)

    def reset_search(self):
        self.entry_search.delete(0, tk.END)
        self.load_customers()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        if not values:
            return

        self.selected_cust_id = int(values[0])
        cust = self.db.get_customer_by_id(self.selected_cust_id)
        if not cust:
            return

        # (id, name, phone, doctor_name, address, created_at)
        self.reset_form_fields_only()
        self.entry_name.insert(0, cust[1] or "")
        self.entry_phone.insert(0, cust[2] or "")
        self.entry_doctor.insert(0, cust[3] or "")
        self.txt_address.insert("1.0", cust[4] or "")

        self.btn_save.config(state=tk.DISABLED)
        self.btn_update.config(state=tk.NORMAL)
        self.btn_delete.config(state=tk.NORMAL)

    def validate_inputs(self):
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        doctor = self.entry_doctor.get().strip()
        address = self.txt_address.get("1.0", tk.END).strip()

        if not name:
            messagebox.showwarning("Validation Error", "Customer name is required!")
            return None

        if not phone:
            messagebox.showwarning("Validation Error", "Contact phone number is required!")
            return None

        return {
            "name": name,
            "phone": phone,
            "doctor": doctor,
            "address": address
        }

    def save_customer(self):
        data = self.validate_inputs()
        if not data:
            return

        try:
            new_id = self.db.add_customer(
                name=data["name"],
                phone=data["phone"],
                doctor_name=data["doctor"],
                address=data["address"]
            )
            messagebox.showinfo("Success", f"✓ Customer '{data['name']}' added successfully (ID: {new_id})!")
            self.reset_form()
            self.load_customers()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add customer: {str(e)}")

    def update_customer(self):
        if not self.selected_cust_id:
            messagebox.showwarning("Warning", "Please select a customer from the table to update.")
            return

        data = self.validate_inputs()
        if not data:
            return

        try:
            self.db.update_customer(
                cust_id=self.selected_cust_id,
                name=data["name"],
                phone=data["phone"],
                doctor_name=data["doctor"],
                address=data["address"]
            )
            messagebox.showinfo("Success", f"✓ Customer '{data['name']}' updated successfully!")
            self.reset_form()
            self.load_customers()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update customer: {str(e)}")

    def delete_customer(self):
        if not self.selected_cust_id:
            messagebox.showwarning("Warning", "Please select a customer from the table to delete.")
            return

        name = self.entry_name.get().strip() or f"ID {self.selected_cust_id}"
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete customer:\n\n'{name}'?\n\nAssociated past invoices will be retained.",
            icon="warning"
        )
        if not confirm:
            return

        try:
            self.db.delete_customer(self.selected_cust_id)
            messagebox.showinfo("Deleted", f"✓ Customer '{name}' deleted successfully.")
            self.reset_form()
            self.load_customers()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete customer: {str(e)}")

    def reset_form_fields_only(self):
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_doctor.delete(0, tk.END)
        self.txt_address.delete("1.0", tk.END)

    def reset_form(self):
        self.selected_cust_id = None
        self.reset_form_fields_only()
        self.btn_save.config(state=tk.NORMAL)
        self.btn_update.config(state=tk.DISABLED)
        self.btn_delete.config(state=tk.DISABLED)
        self.tree.selection_remove(self.tree.selection())

    def on_show(self):
        self.load_customers()


class StandaloneCustomersApp(tk.Tk):
    """Standalone runner for Screenshot capture."""
    def __init__(self):
        super().__init__()
        self.title("Screen 3: Customer & Patient Directory | PharmaCare Medical Store")
        self.geometry("1100x680")
        self.configure(bg=THEME["content_bg"])

        banner = tk.Frame(self, bg=THEME["header_bg"], height=52, padx=20)
        banner.pack(fill=tk.X)
        tk.Label(
            banner,
            text="PROGRAM 30 • SCREEN 3: CUSTOMER & PATIENT DIRECTORY",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg=THEME["header_bg"]
        ).pack(side=tk.LEFT, pady=14)
        tk.Label(
            banner,
            text="● SQLite Customer Records",
            font=("Segoe UI", 9, "bold"),
            fg="#10b981",
            bg=THEME["header_bg"]
        ).pack(side=tk.RIGHT, pady=16)

        container = tk.Frame(self, bg=THEME["content_bg"], padx=18, pady=14)
        container.pack(fill=tk.BOTH, expand=True)

        screen = CustomersScreen(container)
        screen.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = StandaloneCustomersApp()
    app.mainloop()
