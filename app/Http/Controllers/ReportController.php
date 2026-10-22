<?php

namespace App\Http\Controllers;

use App\Models\Book;
use App\Models\Category;
use App\Models\BorrowRecord;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Http\Request;

class ReportController extends Controller
{
    /**
     * Display executive analytics and summary report.
     */
    public function index()
    {
        // 1. Summary Metrics
        $summary = [
            'total_books' => Book::count(),
            'total_copies' => Book::sum('total_copies'),
            'available_copies' => Book::sum('available_copies'),
            'borrowed_copies' => Book::sum('total_copies') - Book::sum('available_copies'),
            'total_members' => User::where('role', 'member')->count(),
            'active_loans' => BorrowRecord::where('status', 'issued')->count(),
            'overdue_loans' => BorrowRecord::where('status', 'overdue')->count(),
            'returned_loans' => BorrowRecord::where('status', 'returned')->count(),
            'total_fines' => BorrowRecord::sum('fine_amount'),
        ];

        // 2. Category Distribution Report
        $categoriesReport = Category::withCount('books')
            ->with(['books'])
            ->get()
            ->map(function ($cat) {
                $totalCopies = $cat->books->sum('total_copies');
                $availCopies = $cat->books->sum('available_copies');
                $borrowed = $totalCopies - $availCopies;
                return (object)[
                    'name' => $cat->name,
                    'code' => $cat->code,
                    'titles_count' => $cat->books_count,
                    'total_copies' => $totalCopies,
                    'available_copies' => $availCopies,
                    'borrowed_copies' => $borrowed,
                    'utilization_rate' => $totalCopies > 0 ? round(($borrowed / $totalCopies) * 100, 1) : 0,
                ];
            });

        // 3. Overdue & Critical Loans Report
        $overdueRecords = BorrowRecord::with(['user', 'book'])
            ->whereIn('status', ['overdue', 'issued'])
            ->where('due_date', '<', Carbon::today())
            ->get()
            ->map(function ($record) {
                $days = Carbon::today()->diffInDays(Carbon::parse($record->due_date));
                $calculatedFine = $days * 10.00;
                return (object)[
                    'id' => $record->id,
                    'member_name' => $record->user->name,
                    'member_email' => $record->user->email,
                    'book_title' => $record->book->title,
                    'isbn' => $record->book->isbn,
                    'due_date' => $record->due_date->format('d M Y'),
                    'days_late' => $days,
                    'fine' => $calculatedFine,
                ];
            });

        return view('reports.index', compact('summary', 'categoriesReport', 'overdueRecords'));
    }
}
