<?php

namespace App\Http\Controllers;

use App\Models\Book;
use App\Models\Category;
use Illuminate\Http\Request;

class BookController extends Controller
{
    /**
     * Display a listing of books with search and category filtering.
     */
    public function index(Request $request)
    {
        $query = Book::with('category');

        // Search filter by title, author, or ISBN
        if ($request->filled('search')) {
            $search = $request->input('search');
            $query->where(function ($q) use ($search) {
                $q->where('title', 'like', "%{$search}%")
                  ->orWhere('author', 'like', "%{$search}%")
                  ->orWhere('isbn', 'like', "%{$search}%");
            });
        }

        // Filter by category
        if ($request->filled('category_id')) {
            $query->where('category_id', $request->input('category_id'));
        }

        // Filter by availability
        if ($request->filled('availability')) {
            if ($request->input('availability') === 'in_stock') {
                $query->where('available_copies', '>', 0);
            } elseif ($request->input('availability') === 'out_of_stock') {
                $query->where('available_copies', '<=', 0);
            }
        }

        $books = $query->orderBy('id', 'desc')->paginate(8)->withQueryString();
        $categories = Category::orderBy('name')->get();

        return view('books.index', compact('books', 'categories'));
    }

    /**
     * Show the form for creating a new book.
     */
    public function create()
    {
        $categories = Category::orderBy('name')->get();
        return view('books.create', compact('categories'));
    }

    /**
     * Store a newly created book in storage.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'isbn' => 'required|string|max:50|unique:books,isbn',
            'title' => 'required|string|max:255',
            'author' => 'required|string|max:255',
            'category_id' => 'required|exists:categories,id',
            'publisher' => 'nullable|string|max:255',
            'publication_year' => 'nullable|integer|min:1900|max:' . (date('Y') + 1),
            'total_copies' => 'required|integer|min:1|max:999',
            'rack_location' => 'nullable|string|max:50',
            'description' => 'nullable|string|max:1000',
        ]);

        // When created, available copies initially equals total copies
        $validated['available_copies'] = $validated['total_copies'];

        $book = Book::create($validated);

        return redirect()->route('books.index')
            ->with('success', "Book '{$book->title}' added to catalog successfully!");
    }

    /**
     * Display the specified book.
     */
    public function show(Book $book)
    {
        $book->load(['category', 'borrowRecords.user']);
        return view('books.show', compact('book'));
    }

    /**
     * Show the form for editing the specified book.
     */
    public function edit(Book $book)
    {
        $categories = Category::orderBy('name')->get();
        return view('books.edit', compact('book', 'categories'));
    }

    /**
     * Update the specified book in storage.
     */
    public function update(Request $request, Book $book)
    {
        $validated = $request->validate([
            'isbn' => 'required|string|max:50|unique:books,isbn,' . $book->id,
            'title' => 'required|string|max:255',
            'author' => 'required|string|max:255',
            'category_id' => 'required|exists:categories,id',
            'publisher' => 'nullable|string|max:255',
            'publication_year' => 'nullable|integer|min:1900|max:' . (date('Y') + 1),
            'total_copies' => 'required|integer|min:1|max:999',
            'rack_location' => 'nullable|string|max:50',
            'description' => 'nullable|string|max:1000',
        ]);

        // Adjust available copies based on change in total copies
        $issuedCount = $book->total_copies - $book->available_copies;
        if ($validated['total_copies'] < $issuedCount) {
            return back()->withErrors([
                'total_copies' => "Cannot reduce total copies below currently issued count ({$issuedCount} copies are currently on loan).",
            ])->withInput();
        }

        $validated['available_copies'] = $validated['total_copies'] - $issuedCount;
        $book->update($validated);

        return redirect()->route('books.index')
            ->with('success', "Book '{$book->title}' updated successfully!");
    }

    /**
     * Remove the specified book from storage.
     */
    public function destroy(Book $book)
    {
        // Safety validation: Prevent deleting book if currently on loan
        $activeLoans = $book->activeLoans()->count();
        if ($activeLoans > 0) {
            return back()->with('error', "Cannot delete '{$book->title}' because {$activeLoans} copies are currently on loan to students. Please process returns first.");
        }

        $title = $book->title;
        $book->delete();

        return redirect()->route('books.index')
            ->with('success', "Book '{$title}' removed from catalog successfully!");
    }
}
