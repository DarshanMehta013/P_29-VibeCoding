@extends('layouts.app')

@section('title', 'Library Dashboard')

@section('content')
<!-- Hero Welcome Banner -->
<div class="card bg-white border-0 shadow-sm mb-4">
    <div class="card-body p-4 p-md-4">
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
            <div>
                <h3 class="fw-bold mb-1">
                    <span class="text-primary"><i class="bi bi-book-half me-1"></i> Library Management Portal</span>
                </h3>
                <p class="text-muted mb-0">
                    Welcome back, <strong>{{ Auth::user()->name }}</strong> ({{ ucfirst(Auth::user()->role) }}). All systems and SQLite databases are synchronized.
                </p>
            </div>
            <div class="d-flex flex-wrap gap-2">
                <a href="{{ route('books.create') }}" class="btn btn-primary btn-sm px-3 shadow-sm">
                    <i class="bi bi-plus-circle me-1"></i> Add New Book
                </a>
                <a href="{{ route('borrowings.create') }}" class="btn btn-outline-primary btn-sm px-3">
                    <i class="bi bi-journal-arrow-up me-1"></i> Issue Book
                </a>
                <a href="{{ route('reports.index') }}" class="btn btn-outline-secondary btn-sm px-3">
                    <i class="bi bi-file-earmark-bar-graph me-1"></i> Reports
                </a>
            </div>
        </div>
    </div>
</div>

<!-- KPI Metrics Grid (6 Stat Cards) -->
<div class="row g-3 mb-4">
    <div class="col-6 col-md-4 col-xl-2">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-body p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="text-muted small fw-semibold">Book Titles</span>
                    <span class="badge bg-primary-subtle text-primary p-2 rounded-circle"><i class="bi bi-journal-bookmark fs-6"></i></span>
                </div>
                <h3 class="fw-bold mb-0 text-dark">{{ $totalTitles }}</h3>
                <small class="text-muted" style="font-size: 0.75rem;">Unique ISBN entries</small>
            </div>
        </div>
    </div>

    <div class="col-6 col-md-4 col-xl-2">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-body p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="text-muted small fw-semibold">Total Stock</span>
                    <span class="badge bg-info-subtle text-info p-2 rounded-circle"><i class="bi bi-stack fs-6"></i></span>
                </div>
                <h3 class="fw-bold mb-0 text-dark">{{ $totalCopies }}</h3>
                <small class="text-muted" style="font-size: 0.75rem;">Physical volumes</small>
            </div>
        </div>
    </div>

    <div class="col-6 col-md-4 col-xl-2">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-body p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="text-muted small fw-semibold">Available</span>
                    <span class="badge bg-success-subtle text-success p-2 rounded-circle"><i class="bi bi-check-circle fs-6"></i></span>
                </div>
                <h3 class="fw-bold mb-0 text-success">{{ $availableCopies }}</h3>
                <small class="text-muted" style="font-size: 0.75rem;">Ready on shelves</small>
            </div>
        </div>
    </div>

    <div class="col-6 col-md-4 col-xl-2">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-body p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="text-muted small fw-semibold">Active Loans</span>
                    <span class="badge bg-warning-subtle text-warning p-2 rounded-circle"><i class="bi bi-clock-history fs-6"></i></span>
                </div>
                <h3 class="fw-bold mb-0 text-warning">{{ $activeLoans }}</h3>
                <small class="text-muted" style="font-size: 0.75rem;">Currently issued</small>
            </div>
        </div>
    </div>

    <div class="col-6 col-md-4 col-xl-2">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-body p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="text-muted small fw-semibold">Overdue Loans</span>
                    <span class="badge bg-danger-subtle text-danger p-2 rounded-circle"><i class="bi bi-exclamation-octagon fs-6"></i></span>
                </div>
                <h3 class="fw-bold mb-0 text-danger">{{ $overdueLoans }}</h3>
                <small class="text-muted" style="font-size: 0.75rem;">Fine applicable</small>
            </div>
        </div>
    </div>

    <div class="col-6 col-md-4 col-xl-2">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-body p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="text-muted small fw-semibold">Members</span>
                    <span class="badge bg-secondary-subtle text-secondary p-2 rounded-circle"><i class="bi bi-people fs-6"></i></span>
                </div>
                <h3 class="fw-bold mb-0 text-dark">{{ $totalMembers }}</h3>
                <small class="text-muted" style="font-size: 0.75rem;">Active student accounts</small>
            </div>
        </div>
    </div>
</div>

<!-- Main Dashboard Grid -->
<div class="row g-4">
    <!-- Left Column: Recent Borrowing Transactions -->
    <div class="col-lg-7">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
                <h6 class="fw-bold mb-0 text-dark"><i class="bi bi-arrow-left-right text-primary me-2"></i> Recent Circulation Activity</h6>
                <a href="{{ route('borrowings.index') }}" class="small text-decoration-none fw-semibold">View All History &rarr;</a>
            </div>
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light small">
                        <tr>
                            <th>Student Member</th>
                            <th>Book Title</th>
                            <th>Due Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody class="small">
                        @forelse($recentLoans as $loan)
                        <tr>
                            <td>
                                <div class="fw-semibold text-dark">{{ $loan->user->name }}</div>
                                <div class="text-muted" style="font-size: 0.75rem;">{{ $loan->user->email }}</div>
                            </td>
                            <td>
                                <div class="fw-semibold text-dark">{{ Str::limit($loan->book->title, 28) }}</div>
                                <div class="text-muted" style="font-size: 0.75rem;">ISBN: {{ $loan->book->isbn }}</div>
                            </td>
                            <td>
                                <div>{{ $loan->due_date->format('d M Y') }}</div>
                            </td>
                            <td>
                                @if($loan->status === 'returned')
                                    <span class="badge bg-success-subtle text-success border border-success-subtle">Returned</span>
                                @elseif($loan->status === 'overdue')
                                    <span class="badge bg-danger-subtle text-danger border border-danger-subtle">Overdue</span>
                                @else
                                    <span class="badge bg-warning-subtle text-warning border border-warning-subtle">Issued</span>
                                @endif
                            </td>
                        </tr>
                        @empty
                        <tr>
                            <td colspan="4" class="text-center py-4 text-muted">No borrowing transactions recorded yet.</td>
                        </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Right Column: Catalog Highlights & Quick Management -->
    <div class="col-lg-5">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
                <h6 class="fw-bold mb-0 text-dark"><i class="bi bi-bookmark-star text-primary me-2"></i> Recent Catalog Acquisitions</h6>
                <a href="{{ route('books.index') }}" class="small text-decoration-none fw-semibold">Browse All &rarr;</a>
            </div>
            <div class="card-body p-3">
                <div class="list-group list-group-flush">
                    @forelse($featuredBooks as $book)
                    <div class="list-group-item px-0 py-2 border-bottom">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="me-2">
                                <h6 class="fw-semibold mb-1 text-dark">{{ Str::limit($book->title, 34) }}</h6>
                                <div class="text-muted small">
                                    <i class="bi bi-person me-1"></i> {{ $book->author }} • 
                                    <span class="badge bg-light text-dark border">{{ $book->category->name }}</span>
                                </div>
                            </div>
                            <span class="badge {{ $book->available_copies > 0 ? 'bg-success' : 'bg-danger' }}">
                                {{ $book->available_copies }} / {{ $book->total_copies }}
                            </span>
                        </div>
                    </div>
                    @empty
                    <p class="text-muted text-center py-3">No books added yet.</p>
                    @endforelse
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
