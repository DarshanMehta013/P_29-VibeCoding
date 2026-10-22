<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use App\Models\User;
use App\Models\Category;
use App\Models\Book;
use App\Models\BorrowRecord;
use Carbon\Carbon;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database with sample Library data.
     */
    public function run(): void
    {
        // 1. Seed Users (Admin, Librarian, Members)
        $admin = User::create([
            'name' => 'Darshan Mehta (Admin)',
            'email' => 'admin@librasys.test',
            'password' => Hash::make('password123'),
            'role' => 'admin',
            'phone' => '9876543210',
        ]);

        $librarian = User::create([
            'name' => 'Library Officer (Staff)',
            'email' => 'librarian@librasys.test',
            'password' => Hash::make('password123'),
            'role' => 'librarian',
            'phone' => '9823456780',
        ]);

        $student1 = User::create([
            'name' => 'Vivaan Sharma',
            'email' => 'vivaan@student.test',
            'password' => Hash::make('password123'),
            'role' => 'member',
            'phone' => '9876500001',
        ]);

        $student2 = User::create([
            'name' => 'Meet Patel',
            'email' => 'meet@student.test',
            'password' => Hash::make('password123'),
            'role' => 'member',
            'phone' => '9876500002',
        ]);

        $student3 = User::create([
            'name' => 'Diya Shah',
            'email' => 'diya@student.test',
            'password' => Hash::make('password123'),
            'role' => 'member',
            'phone' => '9876500003',
        ]);

        // 2. Seed Categories
        $catCS = Category::create([
            'name' => 'Computer Science & AI',
            'code' => 'CS-AI',
            'description' => 'Algorithms, machine learning, systems architecture, and programming paradigms.',
        ]);

        $catWeb = Category::create([
            'name' => 'Web Development & Cloud',
            'code' => 'WEB-DEV',
            'description' => 'Full-stack development, Laravel, PHP, APIs, distributed architectures, and DevOps.',
        ]);

        $catData = Category::create([
            'name' => 'Data Science & Databases',
            'code' => 'DATA-DB',
            'description' => 'Relational database theory, SQL, NoSQL, big data processing, and visualization.',
        ]);

        $catSec = Category::create([
            'name' => 'Cybersecurity & Networks',
            'code' => 'SEC-NET',
            'description' => 'Network protocols, cryptography, ethical hacking, and digital forensics.',
        ]);

        // 3. Seed Books
        $book1 = Book::create([
            'isbn' => '978-0132350884',
            'title' => 'Clean Code: A Handbook of Agile Software Craftsmanship',
            'author' => 'Robert C. Martin',
            'category_id' => $catCS->id,
            'publisher' => 'Prentice Hall',
            'publication_year' => 2008,
            'total_copies' => 5,
            'available_copies' => 3,
            'rack_location' => 'Rack A-01',
            'description' => 'Even bad code can function. But if code isn’t clean, it can bring a development organization to its knees.',
        ]);

        $book2 = Book::create([
            'isbn' => '978-1491936160',
            'title' => 'Laravel: Up & Running (A Comprehensive Guide)',
            'author' => 'Matt Stauffer',
            'category_id' => $catWeb->id,
            'publisher' => "O'Reilly Media",
            'publication_year' => 2023,
            'total_copies' => 4,
            'available_copies' => 2,
            'rack_location' => 'Rack W-04',
            'description' => 'Learn the full Laravel ecosystem including Eloquent, Blade, migrations, routing, and testing.',
        ]);

        $book3 = Book::create([
            'isbn' => '978-0262033848',
            'title' => 'Introduction to Algorithms (Fourth Edition)',
            'author' => 'Thomas H. Cormen, Charles E. Leiserson',
            'category_id' => $catCS->id,
            'publisher' => 'MIT Press',
            'publication_year' => 2022,
            'total_copies' => 6,
            'available_copies' => 5,
            'rack_location' => 'Rack A-03',
            'description' => 'The leading world reference and textbook on contemporary computer algorithms.',
        ]);

        $book4 = Book::create([
            'isbn' => '978-1449373320',
            'title' => 'Designing Data-Intensive Applications',
            'author' => 'Martin Kleppmann',
            'category_id' => $catData->id,
            'publisher' => "O'Reilly Media",
            'publication_year' => 2017,
            'total_copies' => 4,
            'available_copies' => 4,
            'rack_location' => 'Rack D-02',
            'description' => 'The big ideas behind reliable, scalable, and maintainable distributed data systems.',
        ]);

        $book5 = Book::create([
            'isbn' => '978-1119642817',
            'title' => 'The Web Application Hacker’s Handbook',
            'author' => 'Dafydd Stuttard, Marcus Pinto',
            'category_id' => $catSec->id,
            'publisher' => 'Wiley',
            'publication_year' => 2020,
            'total_copies' => 3,
            'available_copies' => 3,
            'rack_location' => 'Rack S-05',
            'description' => 'Discovering and exploiting modern security flaws in web applications.',
        ]);

        // 4. Seed Borrow Records (Loans)
        // Record 1: Currently active loan (Issued)
        BorrowRecord::create([
            'user_id' => $student1->id,
            'book_id' => $book1->id,
            'issue_date' => Carbon::now()->subDays(5)->toDateString(),
            'due_date' => Carbon::now()->addDays(9)->toDateString(),
            'return_date' => null,
            'status' => 'issued',
            'fine_amount' => 0.00,
            'remarks' => 'Issued for semester assignment preparation.',
        ]);

        // Record 2: Overdue loan (fine applicable)
        BorrowRecord::create([
            'user_id' => $student2->id,
            'book_id' => $book2->id,
            'issue_date' => Carbon::now()->subDays(20)->toDateString(),
            'due_date' => Carbon::now()->subDays(6)->toDateString(),
            'return_date' => null,
            'status' => 'overdue',
            'fine_amount' => 60.00, // 6 days * Rs 10/day
            'remarks' => 'Overdue by 6 days. Automated reminder sent.',
        ]);

        // Record 3: Returned book loan
        BorrowRecord::create([
            'user_id' => $student3->id,
            'book_id' => $book3->id,
            'issue_date' => Carbon::now()->subDays(15)->toDateString(),
            'due_date' => Carbon::now()->subDays(1)->toDateString(),
            'return_date' => Carbon::now()->subDays(2)->toDateString(),
            'status' => 'returned',
            'fine_amount' => 0.00,
            'remarks' => 'Returned on time in pristine condition.',
        ]);
    }
}
