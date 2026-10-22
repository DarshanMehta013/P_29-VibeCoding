"""
Practical 30 | Screen 4: Invoices History & Receipt Viewer
Can be imported into main.py or run standalone for taking practical screenshots.
Features:
- View all past billing transactions
- Filter by payment mode (Cash, UPI, Card)
- Live search by invoice number, customer name, phone
- Itemized preview of medicines in selected invoice
- Export invoice to printable text receipt (.txt)
- Export all transactions to JSON (.json)
- Void/Delete invoice with automatic medicine stock restoration
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import DatabaseManager

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


class InvoicesScreen(tk.Frame):
    """Invoice History, Itemized Bill Breakdown, and Receipt Management."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg=THEME["content_bg"])
        self.controller = controller
        self.db = controller.db if controller else DatabaseManager()

        self.selected_invoice_id = None
        self.build_ui()
        self.load_invoices()

    def build_ui(self):
        main_box = tk.Frame(self, bg=THEME["content_bg"])
        main_box.pack(fill=tk.BOTH, expand=True)

        # ------------------ TOP SEARCH & FILTER BAR ------------------
        top_bar = tk.Frame(main_box, bg="#ffffff", padx=14, pady=10, highlightbackground=THEME["card_border"], highlightthickness=1)
        top_bar.pack(fill=tk.X, pady=(0, 10))

        tk.Label(top_bar, text="🔍 Search Invoice:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 6))
        self.entry_search = ttk.Entry(top_bar, font=("Segoe UI", 9), width=22)
        self.entry_search.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_search.bind("<KeyRelease>", lambda e: self.filter_invoices())

        tk.Label(top_bar, text="Payment Mode:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg=THEME["text_dark"]).pack(side=tk.LEFT, padx=(0, 6))
        self.combo_payment = ttk.Combobox(top_bar, values=["All", "Cash", "UPI", "Card"], font=("Segoe UI", 9), state="readonly", width=10)
        self.combo_payment.set("All")
        self.combo_payment.pack(side=tk.LEFT, padx=(0, 10))
        self.combo_payment.bind("<<ComboboxSelected>>", lambda e: self.filter_invoices())

        btn_reset = tk.Button(
            top_bar,
            text="Reset Filter",
            font=("Segoe UI", 8),
            bg="#f1f5f9",
            fg=THEME["text_dark"],
            relief="flat",
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.reset_filters
        )
        btn_reset.pack(side=tk.LEFT, padx=(0, 14))

        # Action Buttons on Right
        btn_json = tk.Button(
            top_bar,
            text="📑 Export JSON",
            font=("Segoe UI", 8, "bold"),
            bg="#f0fdf4",
            fg="#16a34a",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.export_json
        )
        btn_json.pack(side=tk.RIGHT, padx=(4, 0))

        self.btn_receipt = tk.Button(
            top_bar,
            text="🖨️ Save Receipt (.txt)",
            font=("Segoe UI", 8, "bold"),
            bg="#eff6ff",
            fg="#2563eb",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.save_text_receipt
        )
        self.btn_receipt.pack(side=tk.RIGHT, padx=4)

        self.btn_void = tk.Button(
            top_bar,
            text="🗑️ Void Invoice",
            font=("Segoe UI", 8, "bold"),
            bg="#fef2f2",
            fg="#dc2626",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.void_invoice
        )
        self.btn_void.pack(side=tk.RIGHT, padx=4)

        # ------------------ SPLIT WORKSPACE: INVOICES TABLE & ITEM DETAILS ------------------
        split_pane = tk.PanedWindow(main_box, orient=tk.VERTICAL, bg=THEME["card_border"], sashwidth=4)
        split_pane.pack(fill=tk.BOTH, expand=True)

        # Top Pane: Master Invoices List
        top_pane = tk.Frame(split_pane, bg="#ffffff")
        split_pane.add(top_pane, minsize=200)

        columns = ("id", "inv_no", "customer", "phone", "date", "subtotal", "tax", "discount", "net_total", "payment")
        self.tree_invoices = ttk.Treeview(
            top_pane,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )

        self.tree_invoices.heading("id", text="ID")
        self.tree_invoices.heading("inv_no", text="Invoice #")
        self.tree_invoices.heading("customer", text="Customer Name")
        self.tree_invoices.heading("phone", text="Phone")
        self.tree_invoices.heading("date", text="Date & Time")
        self.tree_invoices.heading("subtotal", text="Subtotal")
        self.tree_invoices.heading("tax", text="GST")
        self.tree_invoices.heading("discount", text="Discount")
        self.tree_invoices.heading("net_total", text="Net Total")
        self.tree_invoices.heading("payment", text="Payment")

        self.tree_invoices.column("id", width=35, anchor="center")
        self.tree_invoices.column("inv_no", width=120, anchor="center")
        self.tree_invoices.column("customer", width=140, anchor="w")
        self.tree_invoices.column("phone", width=105, anchor="center")
        self.tree_invoices.column("date", width=130, anchor="center")
        self.tree_invoices.column("subtotal", width=75, anchor="e")
        self.tree_invoices.column("tax", width=65, anchor="e")
        self.tree_invoices.column("discount", width=65, anchor="e")
        self.tree_invoices.column("net_total", width=85, anchor="e")
        self.tree_invoices.column("payment", width=75, anchor="center")

        scroll_inv_y = ttk.Scrollbar(top_pane, orient=tk.VERTICAL, command=self.tree_invoices.yview)
        self.tree_invoices.configure(yscrollcommand=scroll_inv_y.set)

        self.tree_invoices.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_inv_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_invoices.bind("<<TreeviewSelect>>", self.on_invoice_selected)

        # Bottom Pane: Itemized Breakdown of Selected Invoice
        bottom_pane = tk.Frame(split_pane, bg="#ffffff", padx=14, pady=10)
        split_pane.add(bottom_pane, minsize=160)

        bot_header = tk.Frame(bottom_pane, bg="#ffffff")
        bot_header.pack(fill=tk.X, pady=(0, 6))

        self.lbl_detail_title = tk.Label(
            bot_header,
            text="📦 Itemized Breakdown (Select an invoice above to view details)",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg=THEME["primary"]
        )
        self.lbl_detail_title.pack(side=tk.LEFT)

        self.lbl_detail_summary = tk.Label(
            bot_header,
            text="",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=THEME["text_muted"]
        )
        self.lbl_detail_summary.pack(side=tk.RIGHT)

        item_cols = ("item_id", "medicine_name", "batch", "qty", "price", "total")
        self.tree_items = ttk.Treeview(
            bottom_pane,
            columns=item_cols,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )

        self.tree_items.heading("item_id", text="#")
        self.tree_items.heading("medicine_name", text="Medicine / Item")
        self.tree_items.heading("batch", text="Batch No.")
        self.tree_items.heading("qty", text="Quantity")
        self.tree_items.heading("price", text="Unit Price (₹)")
        self.tree_items.heading("total", text="Total Price (₹)")

        self.tree_items.column("item_id", width=35, anchor="center")
        self.tree_items.column("medicine_name", width=200, anchor="w")
        self.tree_items.column("batch", width=110, anchor="center")
        self.tree_items.column("qty", width=80, anchor="center")
        self.tree_items.column("price", width=95, anchor="e")
        self.tree_items.column("total", width=110, anchor="e")

        scroll_items_y = ttk.Scrollbar(bottom_pane, orient=tk.VERTICAL, command=self.tree_items.yview)
        self.tree_items.configure(yscrollcommand=scroll_items_y.set)

        self.tree_items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_items_y.pack(side=tk.RIGHT, fill=tk.Y)

    def load_invoices(self, records=None):
        for item in self.tree_invoices.get_children():
            self.tree_invoices.delete(item)

        if records is None:
            records = self.db.get_all_invoices()

        for r in records:
            # (id, invoice_no, customer_name, customer_phone, date, subtotal, tax_amount, discount, net_total, payment_mode)
            inv_id = r[0]
            inv_no = r[1]
            c_name = r[2]
            c_phone = r[3] or "—"
            inv_date = r[4][:16] if r[4] else "—"
            subtotal = f"₹{r[5]:.2f}"
            tax = f"₹{r[6]:.2f}"
            disc = f"₹{r[7]:.2f}"
            net = f"₹{r[8]:.2f}"
            pay = r[9]

            self.tree_invoices.insert("", tk.END, values=(inv_id, inv_no, c_name, c_phone, inv_date, subtotal, tax, disc, net, pay))

        self.clear_items_table()

    def filter_invoices(self):
        q = self.entry_search.get().strip()
        mode = self.combo_payment.get()
        records = self.db.search_invoices(q, mode)
        self.load_invoices(records)

    def reset_filters(self):
        self.entry_search.delete(0, tk.END)
        self.combo_payment.set("All")
        self.load_invoices()

    def clear_items_table(self):
        for item in self.tree_items.get_children():
            self.tree_items.delete(item)
        self.selected_invoice_id = None
        self.lbl_detail_title.config(text="📦 Itemized Breakdown (Select an invoice above to view details)")
        self.lbl_detail_summary.config(text="")
        self.btn_receipt.config(state=tk.DISABLED)
        self.btn_void.config(state=tk.DISABLED)

    def on_invoice_selected(self, event):
        selected = self.tree_invoices.selection()
        if not selected:
            return

        values = self.tree_invoices.item(selected[0], "values")
        if not values:
            return

        self.selected_invoice_id = int(values[0])
        inv_data = self.db.get_invoice_by_id(self.selected_invoice_id)
        if not inv_data:
            return

        inv_header, items = inv_data
        # inv_header: (id, invoice_no, customer_id, name, phone, doctor, address, date, subtotal, tax, disc, net, pay_mode)
        self.lbl_detail_title.config(
            text=f"📦 Items for {inv_header[1]} | Customer: {inv_header[3]} (Doctor: {inv_header[5] or '—'})"
        )
        self.lbl_detail_summary.config(
            text=f"Net Bill: ₹{inv_header[11]:.2f} via {inv_header[12]}"
        )

        for item in self.tree_items.get_children():
            self.tree_items.delete(item)

        for idx, it in enumerate(items, 1):
            # (ii.id, m.name, m.batch_no, ii.quantity, ii.unit_price, ii.total_price)
            name = it[1]
            batch = it[2]
            qty = it[3]
            price = f"₹{it[4]:.2f}"
            tot = f"₹{it[5]:.2f}"
            self.tree_items.insert("", tk.END, values=(idx, name, batch, qty, price, tot))

        self.btn_receipt.config(state=tk.NORMAL)
        self.btn_void.config(state=tk.NORMAL)

    def save_text_receipt(self):
        if not self.selected_invoice_id:
            messagebox.showwarning("Warning", "Please select an invoice first.")
            return

        inv_data = self.db.get_invoice_by_id(self.selected_invoice_id)
        if not inv_data:
            return

        inv_no = inv_data[0][1]
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Receipt", "*.txt"), ("All files", "*.*")],
            initialfile=f"receipt_{inv_no}.txt",
            title="Save Printable Medical Store Receipt"
        )
        if file_path:
            self.db.generate_text_receipt(self.selected_invoice_id, file_path)
            messagebox.showinfo("Receipt Exported", f"✓ Receipt successfully saved to:\n{file_path}")

    def export_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="sales_history.json",
            title="Export Sales Invoices to JSON"
        )
        if file_path:
            count = self.db.export_invoices_json(file_path)
            messagebox.showinfo("Export Successful", f"✓ Successfully exported {count} sales transactions to JSON:\n{file_path}")

    def void_invoice(self):
        if not self.selected_invoice_id:
            messagebox.showwarning("Warning", "Please select an invoice to void/delete.")
            return

        inv_data = self.db.get_invoice_by_id(self.selected_invoice_id)
        if not inv_data:
            return

        inv_no = inv_data[0][1]
        confirm = messagebox.askyesno(
            "Confirm Void Invoice",
            f"Are you sure you want to void and delete Invoice '{inv_no}'?\n\n"
            f"• All medicines billed will be restored back to inventory stock.\n"
            f"• This action cannot be reversed.",
            icon="warning"
        )
        if not confirm:
            return

        try:
            self.db.delete_invoice(self.selected_invoice_id)
            messagebox.showinfo("Invoice Voided", f"✓ Invoice '{inv_no}' voided. Stock has been rolled back to inventory.")
            self.load_invoices()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to void invoice: {str(e)}")

    def on_show(self):
        self.load_invoices()


class StandaloneInvoicesApp(tk.Tk):
    """Standalone runner for Screenshot capture."""
    def __init__(self):
        super().__init__()
        self.title("Screen 4: Sales Invoices History | PharmaCare Medical Store")
        self.geometry("1140x690")
        self.configure(bg=THEME["content_bg"])

        banner = tk.Frame(self, bg=THEME["header_bg"], height=52, padx=20)
        banner.pack(fill=tk.X)
        tk.Label(
            banner,
            text="PROGRAM 30 • SCREEN 4: SALES INVOICES & RECEIPT MANAGEMENT",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg=THEME["header_bg"]
        ).pack(side=tk.LEFT, pady=14)
        tk.Label(
            banner,
            text="● Relational Join & Stock Rollback",
            font=("Segoe UI", 9, "bold"),
            fg="#10b981",
            bg=THEME["header_bg"]
        ).pack(side=tk.RIGHT, pady=16)

        container = tk.Frame(self, bg=THEME["content_bg"], padx=18, pady=14)
        container.pack(fill=tk.BOTH, expand=True)

        screen = InvoicesScreen(container)
        screen.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = StandaloneInvoicesApp()
    app.mainloop()
