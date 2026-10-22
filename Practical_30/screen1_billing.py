"""
Practical 30 | Screen 1: POS Billing & Cash Register Terminal
Can be imported into main.py or run standalone for taking practical screenshots.
"""

import os
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


class BillingScreen(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.db = controller.db if controller else DatabaseManager()

        # Cart State: list of dicts {med_id, name, batch, price, qty, line_total}
        self.cart = []
        self.selected_customer_id = None

        self.build_ui()
        self.load_initial_data()

    def build_ui(self):
        # Top Container Split: Left (Billing Controls) & Right (Cart Summary)
        main_box = tk.Frame(self, bg=THEME["content_bg"])
        main_box.pack(fill=tk.BOTH, expand=True)

        left_col = tk.Frame(main_box, bg=THEME["content_bg"])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_col = tk.Frame(main_box, bg=THEME["content_bg"], width=340)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_col.pack_propagate(False)

        # ----------------- LEFT COLUMN: CUSTOMER & ITEM SELECTION -----------------
        # 1. Customer Details Card
        cust_card = tk.LabelFrame(left_col, text=" 👤 Customer & Prescription Details ", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["primary"], padx=14, pady=10)
        cust_card.pack(fill=tk.X, pady=(0, 10))

        c_row1 = tk.Frame(cust_card, bg="#ffffff")
        c_row1.pack(fill=tk.X, pady=2)

        tk.Label(c_row1, text="Select Customer:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 8))
        self.combo_customers = ttk.Combobox(c_row1, font=("Segoe UI", 9), state="readonly", width=35)
        self.combo_customers.pack(side=tk.LEFT, padx=(0, 10))
        self.combo_customers.bind("<<ComboboxSelected>>", self.on_customer_selected)

        self.lbl_cust_details = tk.Label(c_row1, text="Phone: — | Doctor: —", font=("Segoe UI", 8), bg="#ffffff", fg=THEME["text_muted"])
        self.lbl_cust_details.pack(side=tk.LEFT)

        # 2. Add Medicine to Cart Card
        item_card = tk.LabelFrame(left_col, text=" 💊 Add Medicines to Billing Cart ", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["primary"], padx=14, pady=10)
        item_card.pack(fill=tk.X, pady=(0, 10))

        i_row1 = tk.Frame(item_card, bg="#ffffff")
        i_row1.pack(fill=tk.X, pady=4)

        tk.Label(i_row1, text="Select Medicine:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 8))
        self.combo_medicines = ttk.Combobox(i_row1, font=("Segoe UI", 9), state="readonly", width=42)
        self.combo_medicines.pack(side=tk.LEFT, padx=(0, 10))
        self.combo_medicines.bind("<<ComboboxSelected>>", self.on_medicine_selected)

        self.lbl_stock_badge = tk.Label(i_row1, text="Stock: — | Price: —", font=("Segoe UI", 8, "bold"), bg="#f1f5f9", fg=THEME["primary"], padx=8, pady=2)
        self.lbl_stock_badge.pack(side=tk.LEFT)

        i_row2 = tk.Frame(item_card, bg="#ffffff")
        i_row2.pack(fill=tk.X, pady=(8, 4))

        tk.Label(i_row2, text="Quantity:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 8))
        self.spin_qty = ttk.Spinbox(i_row2, from_=1, to=1000, font=("Segoe UI", 9), width=8)
        self.spin_qty.set(1)
        self.spin_qty.pack(side=tk.LEFT, padx=(0, 14))

        btn_add = tk.Button(i_row2, text="➕ Add to Cart", font=("Segoe UI", 9, "bold"), bg=THEME["primary"], fg="#ffffff", relief="flat", padx=14, pady=4, cursor="hand2", command=self.add_item_to_cart)
        btn_add.pack(side=tk.LEFT, padx=(0, 8))

        btn_clear_cart = tk.Button(i_row2, text="Clear Cart", font=("Segoe UI", 9), bg="#f1f5f9", fg=THEME["text_dark"], relief="flat", padx=10, pady=4, cursor="hand2", command=self.clear_cart)
        btn_clear_cart.pack(side=tk.LEFT)

        # 3. Itemized Cart Table
        cart_card = tk.Frame(left_col, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1)
        cart_card.pack(fill=tk.BOTH, expand=True)

        cols = ("name", "batch", "price", "qty", "total")
        self.tree_cart = ttk.Treeview(cart_card, columns=cols, show="headings", style="Custom.Treeview")
        self.tree_cart.heading("name", text="Medicine Name")
        self.tree_cart.heading("batch", text="Batch No")
        self.tree_cart.heading("price", text="Unit Price (₹)")
        self.tree_cart.heading("qty", text="Qty")
        self.tree_cart.heading("total", text="Total (₹)")

        self.tree_cart.column("name", width=220, anchor="w")
        self.tree_cart.column("batch", width=90, anchor="center")
        self.tree_cart.column("price", width=90, anchor="e")
        self.tree_cart.column("qty", width=60, anchor="center")
        self.tree_cart.column("total", width=100, anchor="e")

        scroll = ttk.Scrollbar(cart_card, orient=tk.VERTICAL, command=self.tree_cart.yview)
        self.tree_cart.configure(yscrollcommand=scroll.set)

        self.tree_cart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0, 10))

        # ----------------- RIGHT COLUMN: BILL SUMMARY & CHECKOUT -----------------
        bill_card = tk.Frame(right_col, bg="#ffffff", highlightbackground=THEME["card_border"], highlightthickness=1, padx=18, pady=16)
        bill_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(bill_card, text="Billing Summary", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(0, 12))

        # Summary rows
        self.lbl_subtotal = self.add_summary_row(bill_card, "Subtotal:")
        self.lbl_tax = self.add_summary_row(bill_card, "GST Tax (12%):")

        # Discount Entry
        disc_frame = tk.Frame(bill_card, bg="#ffffff")
        disc_frame.pack(fill=tk.X, pady=6)
        tk.Label(disc_frame, text="Discount (₹):", font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"]).pack(side=tk.LEFT)
        self.entry_discount = tk.Entry(disc_frame, font=("Segoe UI", 9), width=10, justify="right", bd=1, relief="solid")
        self.entry_discount.insert(0, "0.00")
        self.entry_discount.pack(side=tk.RIGHT)
        self.entry_discount.bind("<KeyRelease>", lambda e: self.recalculate_totals())

        tk.Frame(bill_card, bg=THEME["card_border"], height=1).pack(fill=tk.X, pady=10)

        # Net Total
        total_frame = tk.Frame(bill_card, bg="#ffffff")
        total_frame.pack(fill=tk.X, pady=(0, 14))
        tk.Label(total_frame, text="NET PAYABLE:", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT)
        self.lbl_net_total = tk.Label(total_frame, text="₹ 0.00", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg=THEME["success"])
        self.lbl_net_total.pack(side=tk.RIGHT)

        # Payment Mode
        tk.Label(bill_card, text="Payment Mode:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(anchor="w", pady=(0, 4))
        self.combo_payment = ttk.Combobox(bill_card, font=("Segoe UI", 9), state="readonly", values=["Cash", "UPI", "Card", "Credit / Pay Later"])
        self.combo_payment.set("Cash")
        self.combo_payment.pack(fill=tk.X, pady=(0, 16))

        # Checkout Buttons
        btn_checkout = tk.Button(
            bill_card,
            text="🧾  Generate Bill & Print Receipt",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["success"],
            fg="#ffffff",
            relief="flat",
            pady=10,
            cursor="hand2",
            command=self.checkout_invoice
        )
        btn_checkout.pack(fill=tk.X, pady=(0, 8))

        btn_del_item = tk.Button(
            bill_card,
            text="🗑️ Remove Selected Item",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg=THEME["danger"],
            relief="flat",
            pady=6,
            cursor="hand2",
            command=self.remove_selected_cart_item
        )
        btn_del_item.pack(fill=tk.X)

    def add_summary_row(self, parent, label_text):
        f = tk.Frame(parent, bg="#ffffff")
        f.pack(fill=tk.X, pady=4)
        tk.Label(f, text=label_text, font=("Segoe UI", 9), bg="#ffffff", fg=THEME["text_muted"]).pack(side=tk.LEFT)
        val_lbl = tk.Label(f, text="₹ 0.00", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"])
        val_lbl.pack(side=tk.RIGHT)
        return val_lbl

    def load_initial_data(self):
        # Load Customers
        customers = self.db.get_all_customers()
        self.customers_cache = customers
        cust_options = [f"{c[1]} (Ph: {c[2]})" for c in customers]
        self.combo_customers["values"] = cust_options
        if customers:
            self.combo_customers.current(0)
            self.on_customer_selected()

        # Load Medicines
        medicines = self.db.get_all_medicines()
        self.medicines_cache = medicines
        med_options = [f"{m[2]} [{m[1]}] - ₹{m[5]:.2f} (Stock: {m[6]})" for m in medicines]
        self.combo_medicines["values"] = med_options
        if medicines:
            self.combo_medicines.current(0)
            self.on_medicine_selected()

    def on_show(self):
        self.load_initial_data()

    def on_customer_selected(self, event=None):
        idx = self.combo_customers.current()
        if idx >= 0 and idx < len(self.customers_cache):
            cust = self.customers_cache[idx]
            self.selected_customer_id = cust[0]
            self.lbl_cust_details.config(text=f"Phone: {cust[2]} | Doctor: {cust[3] or 'Self'}")

    def on_medicine_selected(self, event=None):
        idx = self.combo_medicines.current()
        if idx >= 0 and idx < len(self.medicines_cache):
            med = self.medicines_cache[idx]
            self.current_med = med
            self.lbl_stock_badge.config(text=f"Stock: {med[6]} | Price: ₹{med[5]:.2f}")
            self.spin_qty.config(to=max(1, med[6]))

    def add_item_to_cart(self):
        if not hasattr(self, "current_med"):
            return

        try:
            qty = int(self.spin_qty.get())
        except ValueError:
            messagebox.showwarning("Invalid Quantity", "Please enter a valid numeric quantity.")
            return

        if qty <= 0:
            messagebox.showwarning("Invalid Quantity", "Quantity must be greater than zero.")
            return

        available_stock = self.current_med[6]
        # Check existing qty in cart
        existing_qty = sum(item["qty"] for item in self.cart if item["med_id"] == self.current_med[0])
        if (existing_qty + qty) > available_stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Only {available_stock} units available for {self.current_med[2]}.\nAlready in cart: {existing_qty} units."
            )
            return

        price = float(self.current_med[5])
        line_total = round(qty * price, 2)

        # Check if already in cart to increment
        for item in self.cart:
            if item["med_id"] == self.current_med[0]:
                item["qty"] += qty
                item["line_total"] = round(item["qty"] * item["price"], 2)
                self.refresh_cart_table()
                self.recalculate_totals()
                return

        self.cart.append({
            "med_id": self.current_med[0],
            "name": self.current_med[2],
            "batch": self.current_med[1],
            "price": price,
            "qty": qty,
            "line_total": line_total
        })

        self.refresh_cart_table()
        self.recalculate_totals()

    def refresh_cart_table(self):
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)

        for itm in self.cart:
            self.tree_cart.insert("", tk.END, values=(
                itm["name"], itm["batch"], f"{itm['price']:.2f}", itm["qty"], f"{itm['line_total']:.2f}"
            ))

    def remove_selected_cart_item(self):
        selected = self.tree_cart.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an item from the cart to remove.")
            return
        idx = self.tree_cart.index(selected[0])
        if idx < len(self.cart):
            del self.cart[idx]
            self.refresh_cart_table()
            self.recalculate_totals()

    def clear_cart(self):
        self.cart.clear()
        self.refresh_cart_table()
        self.recalculate_totals()

    def recalculate_totals(self):
        subtotal = sum(item["line_total"] for item in self.cart)
        tax = round(subtotal * 0.12, 2) # GST 12%

        try:
            discount = float(self.entry_discount.get().strip() or "0")
        except ValueError:
            discount = 0.0

        net = max(0.0, round(subtotal + tax - discount, 2))

        self.lbl_subtotal.config(text=f"₹ {subtotal:.2f}")
        self.lbl_tax.config(text=f"₹ {tax:.2f}")
        self.lbl_net_total.config(text=f"₹ {net:.2f}")

    def checkout_invoice(self):
        if not self.selected_customer_id:
            messagebox.showwarning("Select Customer", "Please select a customer for this invoice.")
            return

        if not self.cart:
            messagebox.showwarning("Empty Cart", "Cannot checkout an empty billing cart. Add at least one medicine.")
            return

        try:
            discount = float(self.entry_discount.get().strip() or "0")
        except ValueError:
            discount = 0.0

        payment_mode = self.combo_payment.get()

        # Build items list: (med_id, qty, unit_price)
        items_payload = [(itm["med_id"], itm["qty"], itm["price"]) for itm in self.cart]

        try:
            invoice_id, invoice_no = self.db.create_invoice(
                customer_id=self.selected_customer_id,
                items=items_payload,
                tax_rate=12.0,
                discount=discount,
                payment_mode=payment_mode
            )

            # Auto-generate text receipt
            receipt_path = BASE_DIR / f"receipt_{invoice_no}.txt"
            self.db.generate_text_receipt(invoice_id, receipt_path)

            msg = (
                f"✓ Invoice {invoice_no} generated successfully!\n"
                f"Net Amount: {self.lbl_net_total.cget('text')}\n"
                f"Payment Mode: {payment_mode}\n\n"
                f"A printable text receipt was created at:\n{receipt_path.name}"
            )
            messagebox.showinfo("Billing Complete", msg)

            self.clear_cart()
            self.load_initial_data()

        except Exception as e:
            messagebox.showerror("Checkout Error", f"Failed to record invoice: {str(e)}")


class StandaloneBillingApp(tk.Tk):
    """Standalone runner for Screenshot capture."""
    def __init__(self):
        super().__init__()
        self.title("Screen 1: POS Billing Terminal | PharmaCare Medical Store")
        self.geometry("1100x680")
        self.configure(bg=THEME["content_bg"])

        # Banner
        banner = tk.Frame(self, bg=THEME["header_bg"], height=52, padx=20)
        banner.pack(fill=tk.X)
        tk.Label(banner, text="PROGRAM 30 • SCREEN 1: POS BILLING & INVOICE GENERATOR", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg=THEME["header_bg"]).pack(side=tk.LEFT, pady=14)
        tk.Label(banner, text="● Real-Time SQLite Sync", font=("Segoe UI", 9, "bold"), fg="#10b981", bg=THEME["header_bg"]).pack(side=tk.RIGHT, pady=16)

        container = tk.Frame(self, bg=THEME["content_bg"], padx=18, pady=14)
        container.pack(fill=tk.BOTH, expand=True)

        screen = BillingScreen(container)
        screen.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = StandaloneBillingApp()
    app.mainloop()
