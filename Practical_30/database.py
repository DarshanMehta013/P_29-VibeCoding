"""
Program No. 30: Major Project - II
Medical Store Billing System (PharmaCare POS & Inventory)
Database Layer: SQLite3 Relational Engine with 4 Normalized Tables
"""

import os
import csv
import json
import sqlite3
import datetime
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "pharmacare.db"


class DatabaseManager:
    """Manages SQLite connectivity, migrations, CRUD queries, and transactions."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.init_database()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Medicines Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medicines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_no TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    manufacturer TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock_qty INTEGER NOT NULL,
                    expiry_date TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            # 2. Customers Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    doctor_name TEXT,
                    address TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            # 3. Invoices (Sales Billing) Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_no TEXT NOT NULL UNIQUE,
                    customer_id INTEGER NOT NULL,
                    invoice_date TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    tax_amount REAL NOT NULL,
                    discount REAL NOT NULL,
                    net_total REAL NOT NULL,
                    payment_mode TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
                )
            """)

            # 4. Invoice Items Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER NOT NULL,
                    medicine_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total_price REAL NOT NULL,
                    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
                    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE RESTRICT
                )
            """)
            conn.commit()

        # Seed initial sample data if empty
        if self.count_medicines() == 0:
            self.seed_initial_data()

    def seed_initial_data(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Seed Medicines
            medicines = [
                ("BAT-101", "Paracetamol 650mg (Dolo)", "Antipyretic", "Micro Labs", 32.50, 150, "2027-08-31", now),
                ("BAT-102", "Amoxicillin 500mg", "Antibiotics", "Cipla Ltd", 85.00, 80, "2027-04-15", now),
                ("BAT-103", "Azithromycin 500mg", "Antibiotics", "Zydus Cadila", 120.00, 45, "2026-12-31", now),
                ("BAT-104", "Cetirizine 10mg", "Antihistamine", "Sun Pharma", 22.00, 120, "2028-01-30", now),
                ("BAT-105", "Pantoprazole 40mg (Pan-40)", "Gastrointestinal", "Alkem Labs", 95.00, 90, "2027-09-15", now),
                ("BAT-106", "Metformin 500mg (Glycomet)", "Antidiabetic", "USV Ltd", 42.00, 110, "2027-11-20", now),
                ("BAT-107", "Atorvastatin 10mg", "Cardiovascular", "Lupin Pharma", 115.00, 60, "2027-05-10", now),
                ("BAT-108", "Vitamin C & Zinc (Limcee)", "Supplements", "Abbott India", 35.00, 200, "2028-06-30", now),
                ("BAT-109", "Cough Syrup (Ascoril D+)", "Respiratory", "Glenmark", 125.00, 8, "2027-03-15", now), # Low stock (< 10)
                ("BAT-110", "Ibuprofen 400mg (Brufen)", "Analgesics", "Abbott India", 28.00, 5, "2027-02-28", now), # Low stock (< 10)
            ]
            cursor.executemany("""
                INSERT INTO medicines (batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, medicines)

            # Seed Customers
            customers = [
                ("Vivaan Sharma", "9876543210", "Dr. A. K. Verma", "12, Shanti Nagar, Mumbai", now),
                ("Meet Patel", "9823456789", "Dr. S. Mehta", "45, Ring Road, Surat", now),
                ("Diya Shah", "9812345678", "Dr. R. Joshi", "88, CG Road, Ahmedabad", now),
                ("Rohan Gupta", "9898765432", "Dr. M. Chawla", "5, Civil Lines, Delhi", now),
            ]
            cursor.executemany("""
                INSERT INTO customers (name, phone, doctor_name, address, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, customers)

            conn.commit()

            # Seed Sample Past Invoices
            self.create_invoice(
                customer_id=1,
                items=[(1, 2, 32.50), (4, 1, 22.00)], # Dolo x 2, Cetirizine x 1
                tax_rate=12.0,
                discount=5.0,
                payment_mode="UPI",
                custom_date="2026-10-18 11:30:00"
            )
            self.create_invoice(
                customer_id=2,
                items=[(2, 1, 85.00), (5, 2, 95.00)], # Amoxicillin x 1, Pan-40 x 2
                tax_rate=12.0,
                discount=10.0,
                payment_mode="Cash",
                custom_date="2026-10-20 16:45:00"
            )
            self.create_invoice(
                customer_id=3,
                items=[(8, 3, 35.00)], # Limcee x 3
                tax_rate=5.0,
                discount=0.0,
                payment_mode="Card",
                custom_date="2026-10-22 10:15:00"
            )

    # =========================================================================
    # MEDICINES MODULE (CRUD + SEARCH)
    # =========================================================================
    def count_medicines(self):
        with self.get_connection() as conn:
            return conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]

    def get_all_medicines(self):
        with self.get_connection() as conn:
            return conn.execute("""
                SELECT id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at
                FROM medicines ORDER BY id DESC
            """).fetchall()

    def get_medicine_by_id(self, med_id):
        with self.get_connection() as conn:
            return conn.execute("""
                SELECT id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at
                FROM medicines WHERE id = ?
            """, (med_id,)).fetchone()

    def add_medicine(self, batch_no, name, category, manufacturer, price, stock_qty, expiry_date):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO medicines (batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (batch_no.strip(), name.strip(), category.strip(), manufacturer.strip(), float(price), int(stock_qty), expiry_date.strip(), now))
            conn.commit()
            return cursor.lastrowid

    def update_medicine(self, med_id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE medicines
                SET batch_no = ?, name = ?, category = ?, manufacturer = ?, price = ?, stock_qty = ?, expiry_date = ?
                WHERE id = ?
            """, (batch_no.strip(), name.strip(), category.strip(), manufacturer.strip(), float(price), int(stock_qty), expiry_date.strip(), med_id))
            conn.commit()
            return cursor.rowcount

    def delete_medicine(self, med_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
            conn.commit()
            return cursor.rowcount

    def search_medicines(self, query, category="All"):
        q = f"%{query.strip()}%"
        with self.get_connection() as conn:
            if category == "All" or not category:
                return conn.execute("""
                    SELECT id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at
                    FROM medicines
                    WHERE name LIKE ? OR batch_no LIKE ? OR manufacturer LIKE ? OR category LIKE ?
                    ORDER BY id DESC
                """, (q, q, q, q)).fetchall()
            else:
                return conn.execute("""
                    SELECT id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at
                    FROM medicines
                    WHERE (name LIKE ? OR batch_no LIKE ? OR manufacturer LIKE ?) AND category = ?
                    ORDER BY id DESC
                """, (q, q, q, category)).fetchall()

    def get_categories(self):
        with self.get_connection() as conn:
            rows = conn.execute("SELECT DISTINCT category FROM medicines ORDER BY category").fetchall()
            return [r[0] for r in rows if r[0]]

    # =========================================================================
    # CUSTOMERS MODULE (CRUD + SEARCH)
    # =========================================================================
    def count_customers(self):
        with self.get_connection() as conn:
            return conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

    def get_all_customers(self):
        with self.get_connection() as conn:
            return conn.execute("""
                SELECT id, name, phone, doctor_name, address, created_at
                FROM customers ORDER BY id DESC
            """).fetchall()

    def get_customer_by_id(self, cust_id):
        with self.get_connection() as conn:
            return conn.execute("""
                SELECT id, name, phone, doctor_name, address, created_at
                FROM customers WHERE id = ?
            """, (cust_id,)).fetchone()

    def add_customer(self, name, phone, doctor_name, address):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (name, phone, doctor_name, address, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (name.strip(), phone.strip(), doctor_name.strip(), address.strip(), now))
            conn.commit()
            return cursor.lastrowid

    def update_customer(self, cust_id, name, phone, doctor_name, address):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers
                SET name = ?, phone = ?, doctor_name = ?, address = ?
                WHERE id = ?
            """, (name.strip(), phone.strip(), doctor_name.strip(), address.strip(), cust_id))
            conn.commit()
            return cursor.rowcount

    def delete_customer(self, cust_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id = ?", (cust_id,))
            conn.commit()
            return cursor.rowcount

    def search_customers(self, query):
        q = f"%{query.strip()}%"
        with self.get_connection() as conn:
            return conn.execute("""
                SELECT id, name, phone, doctor_name, address, created_at
                FROM customers
                WHERE name LIKE ? OR phone LIKE ? OR doctor_name LIKE ?
                ORDER BY id DESC
            """, (q, q, q)).fetchall()

    # =========================================================================
    # INVOICES & BILLING MODULE (TRANSACTIONS + CRUD)
    # =========================================================================
    def generate_invoice_no(self):
        with self.get_connection() as conn:
            last_id = conn.execute("SELECT MAX(id) FROM invoices").fetchone()[0] or 0
            return f"INV-{datetime.datetime.now().year}-{last_id + 1:04d}"

    def create_invoice(self, customer_id, items, tax_rate=12.0, discount=0.0, payment_mode="Cash", custom_date=None):
        """
        Creates an invoice transaction:
        items is a list of tuples: (medicine_id, quantity, unit_price)
        Deducts stock automatically from medicines table.
        """
        now = custom_date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        invoice_no = self.generate_invoice_no()

        subtotal = sum(qty * price for _, qty, price in items)
        tax_amount = round(subtotal * (tax_rate / 100.0), 2)
        net_total = max(0.0, round(subtotal + tax_amount - discount, 2))

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Insert invoice
            cursor.execute("""
                INSERT INTO invoices (invoice_no, customer_id, invoice_date, subtotal, tax_amount, discount, net_total, payment_mode, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (invoice_no, customer_id, now, subtotal, tax_amount, discount, net_total, payment_mode, now))
            invoice_id = cursor.lastrowid

            # Insert items & decrement stock
            for med_id, qty, unit_price in items:
                line_total = round(qty * unit_price, 2)
                cursor.execute("""
                    INSERT INTO invoice_items (invoice_id, medicine_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                """, (invoice_id, med_id, qty, unit_price, line_total))

                # Decrement stock
                cursor.execute("""
                    UPDATE medicines
                    SET stock_qty = stock_qty - ?
                    WHERE id = ?
                """, (qty, med_id))

            conn.commit()
            return invoice_id, invoice_no

    def get_all_invoices(self):
        with self.get_connection() as conn:
            return conn.execute("""
                SELECT i.id, i.invoice_no, c.name, c.phone, i.invoice_date, i.subtotal, i.tax_amount, i.discount, i.net_total, i.payment_mode
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                ORDER BY i.id DESC
            """).fetchall()

    def get_invoice_by_id(self, invoice_id):
        with self.get_connection() as conn:
            inv = conn.execute("""
                SELECT i.id, i.invoice_no, c.id, c.name, c.phone, c.doctor_name, c.address, i.invoice_date, i.subtotal, i.tax_amount, i.discount, i.net_total, i.payment_mode
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                WHERE i.id = ?
            """, (invoice_id,)).fetchone()

            if not inv:
                return None

            items = conn.execute("""
                SELECT ii.id, m.name, m.batch_no, ii.quantity, ii.unit_price, ii.total_price
                FROM invoice_items ii
                JOIN medicines m ON ii.medicine_id = m.id
                WHERE ii.invoice_id = ?
            """, (invoice_id,)).fetchall()

            return inv, items

    def delete_invoice(self, invoice_id):
        """Rolls back medicine stock and deletes invoice."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Retrieve items to restore inventory
            items = cursor.execute("""
                SELECT medicine_id, quantity FROM invoice_items WHERE invoice_id = ?
            """, (invoice_id,)).fetchall()

            for med_id, qty in items:
                cursor.execute("""
                    UPDATE medicines SET stock_qty = stock_qty + ? WHERE id = ?
                """, (qty, med_id))

            cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
            conn.commit()
            return cursor.rowcount

    def search_invoices(self, query, payment_mode="All"):
        q = f"%{query.strip()}%"
        with self.get_connection() as conn:
            sql = """
                SELECT i.id, i.invoice_no, c.name, c.phone, i.invoice_date, i.subtotal, i.tax_amount, i.discount, i.net_total, i.payment_mode
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                WHERE (i.invoice_no LIKE ? OR c.name LIKE ? OR c.phone LIKE ?)
            """
            params = [q, q, q]
            if payment_mode != "All" and payment_mode:
                sql += " AND i.payment_mode = ?"
                params.append(payment_mode)
            sql += " ORDER BY i.id DESC"
            return conn.execute(sql, params).fetchall()

    # =========================================================================
    # REPORTS & ANALYTICS
    # =========================================================================
    def get_kpi_metrics(self):
        with self.get_connection() as conn:
            total_meds = conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
            total_stock = conn.execute("SELECT SUM(stock_qty) FROM medicines").fetchone()[0] or 0
            low_stock = conn.execute("SELECT COUNT(*) FROM medicines WHERE stock_qty < 10").fetchone()[0]
            total_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
            total_invoices = conn.execute("SELECT COUNT(*) FROM invoices").fetchone()[0]
            total_revenue = conn.execute("SELECT SUM(net_total) FROM invoices").fetchone()[0] or 0.0

            return {
                "total_meds": total_meds,
                "total_stock": total_stock,
                "low_stock": low_stock,
                "total_customers": total_customers,
                "total_invoices": total_invoices,
                "total_revenue": round(total_revenue, 2),
            }

    def get_low_stock_medicines(self, threshold=10):
        with self.get_connection() as conn:
            return conn.execute("""
                SELECT id, batch_no, name, category, manufacturer, price, stock_qty, expiry_date
                FROM medicines
                WHERE stock_qty <= ?
                ORDER BY stock_qty ASC
            """, (threshold,)).fetchall()

    def get_category_sales_breakdown(self):
        with self.get_connection() as conn:
            return conn.execute("""
                SELECT m.category, COUNT(DISTINCT m.id) as title_count, SUM(m.stock_qty) as total_units,
                       COALESCE(SUM(ii.quantity), 0) as units_sold,
                       COALESCE(SUM(ii.total_price), 0.0) as revenue
                FROM medicines m
                LEFT JOIN invoice_items ii ON m.id = ii.medicine_id
                GROUP BY m.category
                ORDER BY revenue DESC
            """).fetchall()

    # =========================================================================
    # FILE HANDLING (EXPORT & IMPORT: CSV, JSON, TEXT RECEIPT)
    # =========================================================================
    def export_medicines_csv(self, file_path):
        """Exports medicines inventory to CSV format."""
        meds = self.get_all_medicines()
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Batch No", "Medicine Name", "Category", "Manufacturer", "Price (INR)", "Stock Quantity", "Expiry Date", "Recorded Date"])
            writer.writerows(meds)
        return len(meds)

    def import_medicines_csv(self, file_path):
        """Reads CSV and imports new/updated medicine stock back into application."""
        count = 0
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for row in reader:
                    batch = row.get("Batch No") or row.get("batch_no")
                    name = row.get("Medicine Name") or row.get("name")
                    cat = row.get("Category") or row.get("category") or "General"
                    mfg = row.get("Manufacturer") or row.get("manufacturer") or "Generic"
                    price = float(row.get("Price (INR)") or row.get("price") or 0.0)
                    qty = int(row.get("Stock Quantity") or row.get("stock_qty") or 0)
                    exp = row.get("Expiry Date") or row.get("expiry_date") or "2028-12-31"

                    if batch and name:
                        cursor.execute("""
                            INSERT INTO medicines (batch_no, name, category, manufacturer, price, stock_qty, expiry_date, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(batch_no) DO UPDATE SET
                                name=excluded.name,
                                category=excluded.category,
                                manufacturer=excluded.manufacturer,
                                price=excluded.price,
                                stock_qty=medicines.stock_qty + excluded.stock_qty,
                                expiry_date=excluded.expiry_date
                        """, (batch.strip(), name.strip(), cat.strip(), mfg.strip(), price, qty, exp.strip(), now))
                        count += 1
                conn.commit()
        return count

    def export_invoices_json(self, file_path):
        """Exports full transaction history with itemized line details to JSON."""
        invoices = self.get_all_invoices()
        data = []
        for inv in invoices:
            full_inv, items = self.get_invoice_by_id(inv[0])
            data.append({
                "invoice_no": full_inv[1],
                "customer": {
                    "name": full_inv[3],
                    "phone": full_inv[4],
                    "doctor": full_inv[5],
                    "address": full_inv[6],
                },
                "invoice_date": full_inv[7],
                "subtotal": full_inv[8],
                "tax_amount": full_inv[9],
                "discount": full_inv[10],
                "net_total": full_inv[11],
                "payment_mode": full_inv[12],
                "items": [
                    {
                        "medicine_name": itm[1],
                        "batch_no": itm[2],
                        "quantity": itm[3],
                        "unit_price": itm[4],
                        "line_total": itm[5],
                    } for itm in items
                ]
            })

        with open(file_path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return len(data)

    def generate_text_receipt(self, invoice_id, file_path):
        """Generates a formatted printable text receipt file."""
        result = self.get_invoice_by_id(invoice_id)
        if not result:
            return False

        inv, items = result
        receipt = []
        receipt.append("=" * 52)
        receipt.append("          PHARMACARE MEDICAL STORE & CLINIC        ")
        receipt.append("     Opp. City Hospital, Station Road, Ahmedabad    ")
        receipt.append("            Phone: +91 98765 43210                  ")
        receipt.append("=" * 52)
        receipt.append(f"Invoice No : {inv[1]:<20} Date: {inv[7]}")
        receipt.append(f"Customer   : {inv[3]:<20} Phone: {inv[4]}")
        if inv[5]:
            receipt.append(f"Doctor     : {inv[5]}")
        receipt.append("-" * 52)
        receipt.append(f"{'Item Description':<24} {'Qty':<5} {'Price':<8} {'Total':<10}")
        receipt.append("-" * 52)
        for itm in items:
            name_abbr = (itm[1][:22] + "..") if len(itm[1]) > 24 else itm[1]
            receipt.append(f"{name_abbr:<24} {itm[3]:<5} {itm[4]:<8.2f} {itm[5]:<10.2f}")
        receipt.append("-" * 52)
        receipt.append(f"{'Subtotal:':<38} Rs. {inv[8]:>8.2f}")
        receipt.append(f"{'GST Tax:':<38} Rs. {inv[9]:>8.2f}")
        receipt.append(f"{'Discount:':<38} Rs. {inv[10]:>8.2f}")
        receipt.append("=" * 52)
        receipt.append(f"{'NET AMOUNT PAYABLE:':<38} Rs. {inv[11]:>8.2f}")
        receipt.append(f"Payment Mode: {inv[12].upper()}")
        receipt.append("=" * 52)
        receipt.append("       Thank you for your visit! Get well soon!     ")
        receipt.append("    Medicines once sold can only be exchanged with   ")
        receipt.append("       original bill within 7 days of purchase.     ")
        receipt.append("=" * 52)

        content = "\n".join(receipt)
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(content)
        return content
