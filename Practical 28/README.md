# Program No. 28: Student Record Management System
> **AIM**: To develop a complete desktop CRUD application (mini project with 6–7 pages/forms) integrating GUI, database and AI-assisted code generation.

---

## 📌 Project Overview
The **Student Record Management System** is a desktop application built in **Python** using **Tkinter + ttk** and an embedded **SQLite3** relational database.

### 📸 Dedicated Standalone Page Files (For Practical Screenshots)
Each form can be run individually as its own window so you can easily take clean, focused screenshots for your practical file/report:

| Form # | File Name | Description & Screenshot Focus | Command |
|---|---|---|---|
| **Form 1** | [`page1_dashboard.py`](file:///c:/Vibe%20Coding%20Practicals/Practical%2028/page1_dashboard.py) | **Dashboard**: KPI stat cards, live metrics, and recent registrations preview | `python page1_dashboard.py` |
| **Form 2** | [`page2_add_student.py`](file:///c:/Vibe%20Coding%20Practicals/Practical%2028/page2_add_student.py) | **Add Student**: Registration form with validation & duplicate roll checks | `python page2_add_student.py` |
| **Form 3** | [`page3_view_students.py`](file:///c:/Vibe%20Coding%20Practicals/Practical%2028/page3_view_students.py) | **View Students**: Tabular display with striped rows, sorting, and CSV export | `python page3_view_students.py` |
| **Form 4** | [`page4_update_student.py`](file:///c:/Vibe%20Coding%20Practicals/Practical%2028/page4_update_student.py) | **Update Student**: Record dropdown selection, auto-filled fields & editing | `python page4_update_student.py` |
| **Form 5** | [`page5_delete_student.py`](file:///c:/Vibe%20Coding%20Practicals/Practical%2028/page5_delete_student.py) | **Delete Student**: Verification details card & confirmation prompt | `python page5_delete_student.py` |
| **Form 6** | [`page6_search_student.py`](file:///c:/Vibe%20Coding%20Practicals/Practical%2028/page6_search_student.py) | **Search Student**: Multi-field search engine with real-time query results | `python page6_search_student.py` |
| **Form 7** | [`page7_about.py`](file:///c:/Vibe%20Coding%20Practicals/Practical%2028/page7_about.py) | **About Page**: Practical Aim, technologies used, and developer profile | `python page7_about.py` |

---

### 🚀 Quick Screenshot Launcher
You can also launch the interactive menu launcher to open any page with a single click:

```bash
python run_screenshot_runner.py
```

### 🖥️ Full Integrated Application
To run the full multi-page system with sidebar navigation:

```bash
python student_management_system.py
```

---

## 🗄️ Database Architecture
All pages connect to the shared local database `student_records.db` managed by [`db.py`](file:///c:/Vibe%20Coding%20Practicals/Practical%2028/db.py):

```sql
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    course TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```
