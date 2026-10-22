@extends('layouts.app')

@section('title', $book->title)

@section('content')
<div class="row justify-content-center">
    <div class="col-lg-10">
        <div class="d-flex align-items-center justify-content-between mb-3">
            <div>
                <a href="{{ route('books.index') }}" class="text-decoration-none small text-muted">
                    <i class="bi bi-arrow-left"></i> Back to Catalog
                </a>
                <h4 class="fw-bold mb-0 text-dark mt-1">{{ $book->title }}</h4>
            </div>
            <div class="btn-group">
                <a href="{{ route('books.edit', $book) }}" class="btn btn-outline-primary btn-sm">
                    <i class="bi bi-pencil me-1"></i> Edit Book
                </a>
                <a href="{{ route('borrowings.create') }}?book_id={{ $book->id }}" class="btn btn-primary btn-sm">
                    <i class="bi bi-journal-arrow-up me-1"></i> Issue to Student
                </a>
            </div>
        </div>

        <div class="row g-4">
            <!-- Book Metadata Card -->
            <div class="col-md-5">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body p-4">
                        <div class="badge bg-primary-subtle text-primary border border-primary-subtle mb-3">
                            {{ $book->category->name }} ({{ $book->category->code }})
                        </div>

                        <h5 class="fw-bold text-dark">{{ $book->title }}</h5>
                        <p class="text-muted small mb-3">by <strong class="text-dark">{{ $book->author }}</strong></p>

                        <div class="p-3 bg-light rounded border mb-3 small">
                            <div class="row mb-2">
                                <div class="col-5 text-muted">ISBN-13:</div>
                                <div class="col-7 font-monospace fw-semibold">{{ $book->isbn }}</div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-5 text-muted">Publisher:</div>
                                <div class="col-7">{{ $book->publisher ?? 'N/A' }}</div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-5 text-muted">Year:</div>
                                <div class="col-7">{{ $book->publication_year ?? 'N/A' }}</div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-5 text-muted">Location:</div>
                                <div class="col-7"><i class="bi bi-geo-alt text-danger"></i> {{ $book->rack_location ?? 'General Shelf' }}</div>
                            </div>
                            <div class="row">
                                <div class="col-5 text-muted">Inventory:</div>
                                <div class="col-7">
                                    <span class="badge {{ $book->available_copies > 0 ? 'bg-success' : 'bg-danger' }}">
                                        {{ $book->available_copies }} available / {{ $book->total_copies }} total
                                    </span>
                                </div>
                            </div>
                        </div>

                        <h6 class="fw-bold small text-dark mb-1">Synopsis:</h6>
                        <p class="text-muted small mb-0">{{ $book->description ?? 'No synopsis recorded.' }}</p>
                    </div>
                </div>
            </div>

            <!-- Circulation History Table -->
            <div class="col-md-7">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-header bg-white border-bottom py-3">
                        <h6 class="fw-bold mb-0 text-dark"><i class="bi bi-clock-history text-primary me-2"></i> Circulation & Borrowing History</h6>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0 small">
                            <thead class="table-light">
                                <tr>
                                    <th>Member Name</th>
                                    <th>Issue Date</th>
                                    <th>Due Date</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                @forelse($book->borrowRecords as $record)
                                <tr>
                                    <td>
                                        <div class="fw-semibold text-dark">{{ $record->user->name }}</div>
                                        <div class="text-muted" style="font-size: 0.75rem;">{{ $record->user->email }}</div>
                                    </td>
                                    <td>{{ $record->issue_date->format('d M Y') }}</td>
                                    <td>{{ $record->due_date->format('d M Y') }}</td>
                                    <td>
                                        @if($record->status === 'returned')
                                            <span class="badge bg-success-subtle text-success border border-success-subtle">Returned</span>
                                        @elseif($record->status === 'overdue')
                                            <span class="badge bg-danger-subtle text-danger border border-danger-subtle">Overdue (₹{{ $record->fine_amount }})</span>
                                        @else
                                            <span class="badge bg-warning-subtle text-warning border border-warning-subtle">Issued</span>
                                        @endif
                                    </td>
                                </tr>
                                @empty
                                <tr>
                                    <td colspan="4" class="text-center py-4 text-muted">No circulation records for this book yet.</td>
                                </tr>
                                @endforelse
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
