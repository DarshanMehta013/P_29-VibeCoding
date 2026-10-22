# Program No. 29: MAJOR PROJECT – I
## Library Management System (LibraSys)
> **AIM**: To develop a complete database-driven web application with user authentication and CRUD modules using Laravel and AI coding assistants, to deploy it on a hosting server using SSH, and to manage further updates through GitHub.

---

## 📌 Project Overview
**LibraSys** is a complete, database-driven web application built with **Laravel 12 (PHP 8.2+)**, **Bootstrap 5**, and **SQLite/MySQL**. It provides an automated, secure platform for educational institutions to catalog books, manage categorizations, handle student book issues and returns, calculate overdue fines, and generate audit reports.

---

## 🏗️ Technical Architecture & Specifications

| Requirement | Implementation Details |
|---|---|
| **Theme Selected** | **Library Management System** |
| **Backend Framework** | Laravel 12.x (PHP 8.2+) with Eloquent ORM |
| **Database Engine** | SQLite3 / MySQL with relational integrity & cascading foreign keys |
| **Frontend Framework** | Blade Templating Engine + Bootstrap 5.3 + Bootstrap Icons |
| **Authentication** | Session-based login/logout, Bcrypt password hashing, Auth middleware |
| **CRUD Modules** | **Module 1:** Books Management • **Module 2:** Book Issue & Return • **Module 3:** Categories |
| **Search & Filters** | Title / Author / ISBN search engine + Category & Stock availability filters |
| **Summary & Reports** | Executive inventory overview + Category utilization + Overdue loans audit |
| **Version Control** | Git & GitHub (`https://github.com/DarshanMehta013/VibeCoding_P4.git`) |
| **Deployment Mode** | Remote Linux Hosting Server via SSH (`git pull` deployment workflow) |

---

## 🗄️ Database Relational Schema (4 Related Tables)

The database exceeds the requirement of 3 related tables with 4 tables linked via primary and foreign keys:

```
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│           categories            │           │              users              │
├─────────────────────────────────┤           ├─────────────────────────────────┤
│ PK  id                          │           │ PK  id                          │
│     name (VARCHAR, UNIQUE)      │           │     name (VARCHAR)              │
│     code (VARCHAR, UNIQUE)      │           │     email (VARCHAR, UNIQUE)     │
│     description (TEXT, NULL)    │           │     password (HASHED)           │
│     timestamps                  │           │     role (admin/librarian/member│
└────────────────┬────────────────┘           │     phone (VARCHAR, NULL)       │
                 │ 1                          │     timestamps                  │
                 │                            └────────────────┬────────────────┘
                 │ hasMany                                     │ 1
                 │                                             │
                 │ belongsTo                                   │ hasMany
┌────────────────▼────────────────┐                            │
│             books               │                            │
├─────────────────────────────────┤                            │
│ PK  id                          │                            │
│     isbn (VARCHAR, UNIQUE)      │                            │
│     title (VARCHAR)             │                            │
│     author (VARCHAR)            │                            │
│ FK  category_id ──► categories  │                            │
│     publisher (VARCHAR)         │                            │
│     publication_year (INT)      │                            │
│     total_copies (INT)          │                            │
│     available_copies (INT)      │                            │
│     rack_location (VARCHAR)     │                            │
│     description (TEXT)          │                            │
│     timestamps                  │                            │
└────────────────┬────────────────┘                            │
                 │ 1                                           │
                 │                                             │
                 │ hasMany                                     │
                 │                                             │
                 │ belongsTo                  belongsTo        │
┌────────────────▼─────────────────────────────────────────────▼────────────────┐
│                               borrow_records                                  │
├───────────────────────────────────────────────────────────────────────────────┤
│ PK  id                                                                        │
│ FK  user_id ──────────────► users.id (Member borrowing the book)             │
│ FK  book_id ──────────────► books.id (Allocated book volume)                  │
│     issue_date (DATE)                                                         │
│     due_date (DATE)                                                           │
│     return_date (DATE, NULLABLE)                                              │
│     status (ENUM/VARCHAR: 'issued', 'returned', 'overdue')                    │
│     fine_amount (DECIMAL 8,2 - ₹10/day for late returns)                      │
│     remarks (TEXT, NULLABLE)                                                  │
│     timestamps                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Demo Login Credentials

For testing and grading evaluation, the database is pre-seeded with the following accounts:

| Role | Email | Password | Access Privileges |
|---|---|---|---|
| **Librarian / Admin** | `admin@librasys.test` | `password123` | Full CRUD access to Books, Issues, Returns, Categories, Reports |
| **Library Officer** | `librarian@librasys.test` | `password123` | Circulation management, issuing and returning books |
| **Student Member** | `vivaan@student.test` | `password123` | Student borrower with active loan |
| **Student Member** | `meet@student.test` | `password123` | Student borrower with overdue loan |

---

## 💻 Module Walkthrough & Features

### 1. User Authentication (Login & Logout)
- **Routes:** `GET /login`, `POST /login`, `GET /register`, `POST /register`, `POST /logout`
- Unauthenticated guests are automatically redirected to `/login` when trying to access administrative modules.
- Form validation protects against brute-force attacks and invalid formats; CSRF tokens prevent cross-site request forgery.

### 2. Module 1: Books Management (Complete CRUD)
- **Create:** `GET /books/create` & `POST /books` — Validate title, author, unique ISBN, and stock.
- **Read:** `GET /books` — Interactive catalog table with book details, rack location, availability badge.
- **Update:** `GET /books/{id}/edit` & `PUT /books/{id}` — Modify book attributes with safety check preventing reducing copies below currently issued count.
- **Delete:** `DELETE /books/{id}` — Modal confirmation. System blocks deletion if active loans exist.

### 3. Module 2: Book Issue & Return (Complete CRUD)
- **Issue (Create):** `GET /borrowings/create` & `POST /borrowings` — Allocates copy to student, automatically decrements `available_copies` on shelf.
- **View (Read):** `GET /borrowings` — Tabbed status filters (**All**, **Active Issued**, **Overdue**, **Returned**).
- **Return (Update):** `POST /borrowings/{id}/return` — Automatically checks return date against due date, calculates overdue fine at **₹10/day**, increments shelf stock.
- **Delete:** `DELETE /borrowings/{id}` — Removes transaction and restores inventory if loan was active.

### 4. Search & Filter Facility
- Search books dynamically by **Title**, **Author**, or **ISBN**.
- Filter books by **Department / Category** and **In-Stock Availability**.
- Filter loans by **Loan Status** and search by **Student Name** or **Email**.

### 5. Report & Summary View
- **Route:** `GET /reports` (`ReportController@index`)
- **Executive Summary:** Aggregated cards for Total Titles, Total Volumes, Books on Shelf, In-Circulation Volumes, and Overdue Penalties.
- **Category Utilization Breakdown:** Table displaying Total Titles, Total Physical Volumes, In Circulation, and percentage utilization rate with visual progress bars.
- **Overdue Loans Audit:** List of all delinquent loans with student contacts, days late, and assessed fines.
- **Print Utility:** Integrated `@media print` CSS for instant one-click PDF / Paper export.

---

## 🌐 Server Deployment via SSH & GitHub Workflow

### Step 1: Push Local Application to GitHub
```bash
cd "c:\Vibe Coding Practicals"
git add .
git commit -m "Implement Program 29: Laravel Library Management System with auth, CRUD, search, reports"
git push origin main
```

### Step 2: Connect to Hosting Server via SSH
```bash
ssh username@your-server-ip
# Or with SSH key:
ssh -i ~/.ssh/id_rsa username@your-server-ip
```

### Step 3: Clone & Configure on Server
```bash
cd /var/www
git clone https://github.com/DarshanMehta013/VibeCoding_P4.git
cd VibeCoding_P4/Practical_29

# Set up environment
cp .env.example .env
nano .env   # Update APP_URL, DB configuration

# Install dependencies and setup keys
composer install --no-dev --optimize-autoloader
php artisan key:generate

# Run database migrations and seed demo data
php artisan migrate --seed --force

# Set file permissions for web server (Nginx/Apache)
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
```

### Step 4: Demonstrating GitHub Update via `git pull`
To demonstrate the requirement of pushing a change to GitHub and applying it via SSH:

1. **On Local Machine (Make a change, e.g., update app version or title):**
   ```bash
   git add .
   git commit -m "Update system banner and fine calculation rate"
   git push origin main
   ```

2. **On Hosting Server via SSH:**
   ```bash
   cd /var/www/VibeCoding_P4/Practical_29
   git pull origin main
   php artisan migrate --force
   php artisan config:cache
   php artisan route:cache
   php artisan view:cache
   ```

---

## 🤖 AI Prompts Used During Development

1. **Ideation & Architecture:**
   > *"Design a database schema for a Laravel Library Management System with 4 related tables: users, categories, books, and borrow_records with foreign keys and cascade actions."*

2. **Migrations & Seeders:**
   > *"Generate Laravel migrations for categories, books, and borrow_records including status enum, fine amount, and seed initial demo books across Computer Science and Web Development."*

3. **Controllers & Validation:**
   > *"Create a Laravel BookController and BorrowRecordController with complete CRUD operations, request validation, shelf availability decrementing on issue, and fine calculation on return."*

4. **Blade Layouts & UI:**
   > *"Build a responsive Bootstrap 5 Blade layout with navigation bar, active link highlighting, flash toast notifications, KPI summary cards, and modal deletion dialogs."*

5. **Search & Analytics Report:**
   > *"Create a ReportController that calculates category utilization percentages, overdue loans count, and lists delinquent borrowers with fine calculations."*
