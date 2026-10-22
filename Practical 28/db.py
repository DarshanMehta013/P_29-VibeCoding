"""
Database Manager for Student Record Management System
Handles SQLite3 CRUD operations and initial seeding.
"""

import sqlite3
import datetime
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
DB_PATH = CURRENT_DIR / "student_records.db"


class DatabaseManager:
    """Handles all SQLite database CRUD operations."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_no TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    course TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

        if self.count_students() == 0:
            sample_data = [
                ("21", "Vivaan Sharma", "Computer Engineering", "vivaan@gmail.com", "9876543210", "2026-10-15 10:30:00"),
                ("55", "Meet Patel", "Computer Engineering", "meet@gmail.com", "9876543211", "2026-10-16 11:45:00"),
                ("101", "Aarav Gupta", "Information Technology", "aarav@gmail.com", "9823456789", "2026-10-18 09:15:00"),
                ("102", "Diya Shah", "Artificial Intelligence & DS", "diya@gmail.com", "9812345678", "2026-10-20 14:20:00"),
                ("103", "Rohan Verma", "Data Science", "rohan@gmail.com", "9898765432", "2026-10-21 16:05:00"),
            ]
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany("""
                    INSERT INTO students (roll_no, name, course, email, phone, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, sample_data)
                conn.commit()

    def count_students(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            return cursor.fetchone()[0]

    def count_courses(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT course) FROM students")
            return cursor.fetchone()[0]

    def get_all_students(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students ORDER BY id DESC")
            return cursor.fetchall()

    def get_recent_students(self, limit=5):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students ORDER BY id DESC LIMIT ?", (limit,))
            return cursor.fetchall()

    def get_student_by_roll(self, roll_no):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE roll_no = ?", (roll_no,))
            return cursor.fetchone()

    def get_student_by_id(self, student_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE id = ?", (student_id,))
            return cursor.fetchone()

    def add_student(self, roll_no, name, course, email, phone):
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (roll_no, name, course, email, phone, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (roll_no, name, course, email, phone, created_at))
            conn.commit()
            return cursor.lastrowid

    def update_student(self, student_id, roll_no, name, course, email, phone):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students
                SET roll_no = ?, name = ?, course = ?, email = ?, phone = ?
                WHERE id = ?
            """, (roll_no, name, course, email, phone, student_id))
            conn.commit()
            return cursor.rowcount

    def delete_student(self, student_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            return cursor.rowcount

    def search_students(self, query, field="all"):
        q = f"%{query.strip()}%"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if field == "roll":
                cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE roll_no LIKE ? ORDER BY id DESC", (q,))
            elif field == "name":
                cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE name LIKE ? ORDER BY id DESC", (q,))
            elif field == "course":
                cursor.execute("SELECT id, roll_no, name, course, email, phone, created_at FROM students WHERE course LIKE ? ORDER BY id DESC", (q,))
            else:
                cursor.execute("""
                    SELECT id, roll_no, name, course, email, phone, created_at
                    FROM students
                    WHERE roll_no LIKE ? OR name LIKE ? OR course LIKE ? OR email LIKE ? OR phone LIKE ?
                    ORDER BY id DESC
                """, (q, q, q, q, q))
            return cursor.fetchall()
