<?php

namespace App\Http\Controllers;

use App\Models\Book;
use App\Models\Category;
use App\Models\BorrowRecord;
use App\Models\User;
use Carbon\Carbon;

class DashboardController extends Controller
{
    /**
     * Show the application dashboard with KPI metrics.
     */
    public function index()
    {
        $totalTitles = Book::count();
        $totalCopies = Book::sum('total_copies');
        $availableCopies = Book::sum('available_copies');
        $activeLoans = BorrowRecord::where('status', 'issued')->count();
        
        // Auto-update overdue records if due_date < today
        BorrowRecord::where('status', 'issued')
            ->where('due_date', '<', Carbon::today())
            ->update(['status' => 'overdue']);

        $overdueLoans = BorrowRecord::where('status', 'overdue')->count();
        $totalMembers = User::where('role', 'member')->count();
        $totalCategories = Category::count();

        $recentLoans = BorrowRecord::with(['user', 'book'])
            ->orderBy('id', 'desc')
            ->take(5)
            ->get();

        $featuredBooks = Book::with('category')
            ->orderBy('id', 'desc')
            ->take(4)
            ->get();

        return view('dashboard', compact(
            'totalTitles',
            'totalCopies',
            'availableCopies',
            'activeLoans',
            'overdueLoans',
            'totalMembers',
            'totalCategories',
            'recentLoans',
            'featuredBooks'
        ));
    }
}
