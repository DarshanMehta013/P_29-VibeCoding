<?php

namespace App\Http\Controllers;

use App\Models\BorrowRecord;
use App\Models\Book;
use App\Models\User;
use Illuminate\Http\Request;
use Carbon\Carbon;

class BorrowRecordController extends Controller
{
    /**
     * Display a listing of borrowing records with status filters.
     */
    public function index(Request $request)
    {
        // Auto-check overdue status
        BorrowRecord::where('status', 'issued')
            ->where('due_date', '<', Carbon::today())
            ->update(['status' => 'overdue']);

        $query = BorrowRecord::with(['user', 'book.category']);

        // Filter by Status
        if ($request->filled('status') && $request->input('status') !== 'all') {
            $query->where('status', $request->input('status'));
        }

        // Search by Member Name or Book Title
        if ($request->filled('search')) {
            $search = $request->input('search');
            $query->where(function ($q) use ($search) {
                $q->whereHas('user', function ($uq) use ($search) {
                    $uq->where('name', 'like', "%{$search}%")
                       ->orWhere('email', 'like', "%{$search}%");
                })->orWhereHas('book', function ($bq) use ($search) {
                    $bq->where('title', 'like', "%{$search}%")
                       ->orWhere('isbn', 'like', "%{$search}%");
                });
            });
        }

        $records = $query->orderBy('id', 'desc')->paginate(10)->withQueryString();

        $stats = [
            'total' => BorrowRecord::count(),
            'issued' => BorrowRecord::where('status', 'issued')->count(),
            'overdue' => BorrowRecord::where('status', 'overdue')->count(),
            'returned' => BorrowRecord::where('status', 'returned')->count(),
        ];

        return view('borrowings.index', compact('records', 'stats'));
    }

    /**
     * Show the form for issuing a new book to a member.
     */
    public function create()
    {
        $members = User::where('role', 'member')->orderBy('name')->get();
        $availableBooks = Book::where('available_copies', '>', 0)->with('category')->orderBy('title')->get();

        return view('borrowings.create', compact('members', 'availableBooks'));
    }

    /**
     * Store a newly issued book record.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'user_id' => 'required|exists:users,id',
            'book_id' => 'required|exists:books,id',
            'issue_date' => 'required|date',
            'due_date' => 'required|date|after_or_equal:issue_date',
            'remarks' => 'nullable|string|max:500',
        ]);

        $book = Book::findOrFail($validated['book_id']);

        if ($book->available_copies <= 0) {
            return back()->withErrors([
                'book_id' => "No copies of '{$book->title}' are currently available in the library.",
            ])->withInput();
        }

        // Check if student already has this book checked out
        $alreadyBorrowed = BorrowRecord::where('user_id', $validated['user_id'])
            ->where('book_id', $validated['book_id'])
            ->whereIn('status', ['issued', 'overdue'])
            ->exists();

        if ($alreadyBorrowed) {
            return back()->withErrors([
                'book_id' => "This member currently already has an active copy of '{$book->title}' checked out.",
            ])->withInput();
        }

        // Deduct available copy
        $book->decrement('available_copies');

        $validated['status'] = 'issued';
        $validated['fine_amount'] = 0.00;

        $record = BorrowRecord::create($validated);

        return redirect()->route('borrowings.index')
            ->with('success', "Book '{$book->title}' has been successfully issued to member.");
    }

    /**
     * Process return of an issued book and calculate fine if overdue.
     */
    public function returnBook(Request $request, BorrowRecord $borrowing)
    {
        if ($borrowing->status === 'returned') {
            return back()->with('error', 'This book has already been marked as returned.');
        }

        $returnDate = Carbon::today();
        $dueDate = Carbon::parse($borrowing->due_date);

        $fine = 0.00;
        if ($returnDate->gt($dueDate)) {
            $daysOverdue = $returnDate->diffInDays($dueDate);
            $fineRatePerDay = 10.00; // Rs 10 per day late fee
            $fine = $daysOverdue * $fineRatePerDay;
        }

        $borrowing->update([
            'return_date' => $returnDate->toDateString(),
            'status' => 'returned',
            'fine_amount' => $fine,
            'remarks' => $request->input('remarks', $borrowing->remarks),
        ]);

        // Increment available copy back
        $borrowing->book->increment('available_copies');

        $msg = "Book '{$borrowing->book->title}' returned successfully.";
        if ($fine > 0) {
            $msg .= " An overdue late fine of ₹" . number_format($fine, 2) . " has been assessed.";
        }

        return redirect()->route('borrowings.index')->with('success', $msg);
    }

    /**
     * Delete a borrowing transaction.
     */
    public function destroy(BorrowRecord $borrowing)
    {
        // If loan was active, restore inventory
        if (in_array($borrowing->status, ['issued', 'overdue'])) {
            $borrowing->book->increment('available_copies');
        }

        $borrowing->delete();

        return redirect()->route('borrowings.index')
            ->with('success', 'Borrowing transaction record deleted successfully.');
    }
}
