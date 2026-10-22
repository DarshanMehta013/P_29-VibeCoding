<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\BookController;
use App\Http\Controllers\BorrowRecordController;
use App\Http\Controllers\CategoryController;
use App\Http\Controllers\ReportController;

// Public Root Redirect
Route::get('/', function () {
    return redirect()->route('dashboard');
});

// Authentication Routes (Guests only)
Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
    Route::post('/login', [AuthController::class, 'login'])->name('login.post');
    Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
    Route::post('/register', [AuthController::class, 'register'])->name('register.post');
});

// Authenticated Routes (Requires Login)
Route::middleware('auth')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

    // Dashboard
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');

    // Module 1: Books Management (CRUD)
    Route::get('/books', [BookController::class, 'index'])->name('books.index');
    Route::get('/books/create', [BookController::class, 'create'])->name('books.create');
    Route::post('/books', [BookController::class, 'store'])->name('books.store');
    Route::get('/books/{book}', [BookController::class, 'show'])->name('books.show');
    Route::get('/books/{book}/edit', [BookController::class, 'edit'])->name('books.edit');
    Route::put('/books/{book}', [BookController::class, 'update'])->name('books.update');
    Route::delete('/books/{book}', [BookController::class, 'destroy'])->name('books.destroy');

    // Module 2: Book Issue & Return / Borrowing Records (CRUD)
    Route::get('/borrowings', [BorrowRecordController::class, 'index'])->name('borrowings.index');
    Route::get('/borrowings/create', [BorrowRecordController::class, 'create'])->name('borrowings.create');
    Route::post('/borrowings', [BorrowRecordController::class, 'store'])->name('borrowings.store');
    Route::post('/borrowings/{borrowing}/return', [BorrowRecordController::class, 'returnBook'])->name('borrowings.return');
    Route::delete('/borrowings/{borrowing}', [BorrowRecordController::class, 'destroy'])->name('borrowings.destroy');

    // Module 3: Categories Management
    Route::get('/categories', [CategoryController::class, 'index'])->name('categories.index');
    Route::post('/categories', [CategoryController::class, 'store'])->name('categories.store');
    Route::put('/categories/{category}', [CategoryController::class, 'update'])->name('categories.update');
    Route::delete('/categories/{category}', [CategoryController::class, 'destroy'])->name('categories.destroy');

    // Reports & Analytics Summary
    Route::get('/reports', [ReportController::class, 'index'])->name('reports.index');
});
