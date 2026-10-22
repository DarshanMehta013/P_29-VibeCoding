@extends('layouts.app')

@section('title', 'Books Catalog & Inventory')

@section('content')
<div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
    <div>
        <h4 class="fw-bold mb-1 text-dark"><i class="bi bi-collection text-primary me-2"></i> Books Catalog Management</h4>
        <p class="text-muted small mb-0">Browse, search, add, and manage physical book inventory and allocations.</p>
    </div>
    <div>
        <a href="{{ route('books.create') }}" class="btn btn-primary px-3 shadow-sm fw-semibold">
            <i class="bi bi-plus-lg me-1"></i> Add New Book
        </a>
    </div>
</div>

<!-- Search & Filtering Strip -->
<div class="card border-0 shadow-sm mb-4">
    <div class="card-body p-3">
        <form method="GET" action="{{ route('books.index') }}" class="row g-2 align-items-center">
            <div class="col-md-5">
                <div class="input-group">
                    <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
                    <input type="text" name="search" class="form-control border-start-0 ps-0" placeholder="Search by Title, Author, or ISBN..." value="{{ request('search') }}">
                </div>
            </div>

            <div class="col-md-3">
                <select name="category_id" class="form-select">
                    <option value="">All Categories / Genres</option>
                    @foreach($categories as $cat)
                        <option value="{{ $cat->id }}" {{ request('category_id') == $cat->id ? 'selected' : '' }}>
                            {{ $cat->name }}
                        </option>
                    @endforeach
                </select>
            </div>

            <div class="col-md-2">
                <select name="availability" class="form-select">
                    <option value="">All Availability</option>
                    <option value="in_stock" {{ request('availability') == 'in_stock' ? 'selected' : '' }}>In Stock Only</option>
                    <option value="out_of_stock" {{ request('availability') == 'out_of_stock' ? 'selected' : '' }}>Out of Stock</option>
                </select>
            </div>

            <div class="col-md-2 d-flex gap-2">
                <button type="submit" class="btn btn-primary w-100 fw-semibold">
                    <i class="bi bi-funnel me-1"></i> Filter
                </button>
                @if(request()->hasAny(['search', 'category_id', 'availability']))
                <a href="{{ route('books.index') }}" class="btn btn-outline-secondary" title="Reset Filters">
                    <i class="bi bi-x-lg"></i>
                </a>
                @endif
            </div>
        </form>
    </div>
</div>

<!-- Books Catalog Table -->
<div class="card border-0 shadow-sm">
    <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
            <thead class="table-light small">
                <tr>
                    <th style="width: 50px;">#</th>
                    <th>Book Details</th>
                    <th>Category</th>
                    <th>ISBN</th>
                    <th>Location</th>
                    <th>Stock / Availability</th>
                    <th class="text-end" style="width: 170px;">Actions</th>
                </tr>
            </thead>
            <tbody>
                @forelse($books as $book)
                <tr>
                    <td class="text-muted small">{{ $book->id }}</td>
                    <td>
                        <div class="d-flex align-items-center">
                            <div class="badge bg-light text-primary border p-2 me-2 fs-6">
                                <i class="bi bi-book"></i>
                            </div>
                            <div>
                                <a href="{{ route('books.show', $book) }}" class="fw-bold text-dark text-decoration-none">
                                    {{ $book->title }}
                                </a>
                                <div class="text-muted small">by <span class="fw-medium text-secondary">{{ $book->author }}</span></div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <span class="badge bg-primary-subtle text-primary border border-primary-subtle">
                            {{ $book->category->name }}
                        </span>
                    </td>
                    <td class="small text-muted font-monospace">{{ $book->isbn }}</td>
                    <td class="small text-muted">
                        <i class="bi bi-geo-alt me-1 text-danger"></i> {{ $book->rack_location ?? 'General Shelf' }}
                    </td>
                    <td>
                        @if($book->available_copies > 0)
                            <span class="badge bg-success-subtle text-success border border-success-subtle">
                                <i class="bi bi-check2-circle me-1"></i> {{ $book->available_copies }} of {{ $book->total_copies }} available
                            </span>
                        @else
                            <span class="badge bg-danger-subtle text-danger border border-danger-subtle">
                                <i class="bi bi-x-circle me-1"></i> All {{ $book->total_copies }} Issued
                            </span>
                        @endif
                    </td>
                    <td class="text-end">
                        <div class="btn-group btn-group-sm">
                            <a href="{{ route('books.show', $book) }}" class="btn btn-outline-secondary" title="View Details">
                                <i class="bi bi-eye"></i>
                            </a>
                            <a href="{{ route('books.edit', $book) }}" class="btn btn-outline-primary" title="Edit Book">
                                <i class="bi bi-pencil"></i>
                            </a>
                            <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteModal{{ $book->id }}" title="Delete Book">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>

                        <!-- Delete Confirmation Modal -->
                        <div class="modal fade" id="deleteModal{{ $book->id }}" tabindex="-1" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered text-start">
                                <div class="modal-content border-0 shadow">
                                    <div class="modal-header bg-danger text-white">
                                        <h6 class="modal-title fw-bold"><i class="bi bi-exclamation-triangle-fill me-2"></i> Confirm Book Deletion</h6>
                                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body p-4">
                                        <p class="mb-2">Are you sure you want to permanently delete this book record from the library catalog?</p>
                                        <div class="p-3 bg-light rounded border mb-2">
                                            <strong>{{ $book->title }}</strong>
                                            <div class="text-muted small">ISBN: {{ $book->isbn }} | Author: {{ $book->author }}</div>
                                        </div>
                                        <small class="text-muted">Note: Books with active loans cannot be deleted until returned.</small>
                                    </div>
                                    <div class="modal-footer bg-light">
                                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
                                        <form method="POST" action="{{ route('books.destroy', $book) }}" class="d-inline">
                                            @csrf
                                            @method('DELETE')
                                            <button type="submit" class="btn btn-danger btn-sm">Yes, Delete Book</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                @empty
                <tr>
                    <td colspan="7" class="text-center py-5 text-muted">
                        <i class="bi bi-journal-x fs-1 d-block mb-2 text-secondary"></i>
                        <h5>No books found</h5>
                        <p class="small mb-3">No catalog entries match your search criteria.</p>
                        <a href="{{ route('books.create') }}" class="btn btn-primary btn-sm">Add First Book</a>
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>

    <!-- Pagination -->
    @if($books->hasPages())
    <div class="card-footer bg-white border-top py-3">
        <div class="d-flex justify-content-between align-items-center">
            <span class="small text-muted">Showing {{ $books->firstItem() }} to {{ $books->lastItem() }} of {{ $books->total() }} books</span>
            <div>{{ $books->links('pagination::bootstrap-5') }}</div>
        </div>
    </div>
    @endif
</div>
@endsection
