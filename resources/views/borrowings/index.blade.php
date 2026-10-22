@extends('layouts.app')

@section('title', 'Book Issue & Return Records')

@section('content')
<div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
    <div>
        <h4 class="fw-bold mb-1 text-dark"><i class="bi bi-arrow-left-right text-primary me-2"></i> Book Circulation & Loan Records</h4>
        <p class="text-muted small mb-0">Track active loans, manage book returns, and compute overdue fines.</p>
    </div>
    <div>
        <a href="{{ route('borrowings.create') }}" class="btn btn-primary px-3 shadow-sm fw-semibold">
            <i class="bi bi-journal-arrow-up me-1"></i> Issue Book to Member
        </a>
    </div>
</div>

<!-- Status Filter Tabs & Search -->
<div class="card border-0 shadow-sm mb-4">
    <div class="card-body p-3">
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
            <!-- Filter Pills -->
            <ul class="nav nav-pills gap-1">
                <li class="nav-item">
                    <a class="nav-link py-1 px-3 {{ !request('status') || request('status') === 'all' ? 'active' : '' }}" href="{{ route('borrowings.index', ['status' => 'all', 'search' => request('search')]) }}">
                        All ({{ $stats['total'] }})
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link py-1 px-3 {{ request('status') === 'issued' ? 'active' : '' }}" href="{{ route('borrowings.index', ['status' => 'issued', 'search' => request('search')]) }}">
                        Active Issued ({{ $stats['issued'] }})
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link py-1 px-3 text-danger {{ request('status') === 'overdue' ? 'active bg-danger text-white' : '' }}" href="{{ route('borrowings.index', ['status' => 'overdue', 'search' => request('search')]) }}">
                        Overdue ({{ $stats['overdue'] }})
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link py-1 px-3 text-success {{ request('status') === 'returned' ? 'active bg-success text-white' : '' }}" href="{{ route('borrowings.index', ['status' => 'returned', 'search' => request('search')]) }}">
                        Returned ({{ $stats['returned'] }})
                    </a>
                </li>
            </ul>

            <!-- Search Form -->
            <form method="GET" action="{{ route('borrowings.index') }}" class="d-flex gap-2">
                @if(request('status'))
                    <input type="hidden" name="status" value="{{ request('status') }}">
                @endif
                <div class="input-group input-group-sm">
                    <span class="input-group-text bg-white"><i class="bi bi-search text-muted"></i></span>
                    <input type="text" name="search" class="form-control" placeholder="Search student or book..." value="{{ request('search') }}">
                    <button type="submit" class="btn btn-outline-secondary">Search</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Circulation Records Table -->
<div class="card border-0 shadow-sm">
    <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
            <thead class="table-light small">
                <tr>
                    <th style="width: 50px;">#</th>
                    <th>Borrower / Member</th>
                    <th>Book Title & Category</th>
                    <th>Issue Date</th>
                    <th>Due Date</th>
                    <th>Return Date</th>
                    <th>Status & Fine</th>
                    <th class="text-end" style="width: 160px;">Actions</th>
                </tr>
            </thead>
            <tbody class="small">
                @forelse($records as $rec)
                <tr>
                    <td class="text-muted">{{ $rec->id }}</td>
                    <td>
                        <div class="fw-bold text-dark">{{ $rec->user->name }}</div>
                        <div class="text-muted" style="font-size: 0.75rem;">
                            <i class="bi bi-envelope me-1"></i> {{ $rec->user->email }}
                            @if($rec->user->phone)
                                • <i class="bi bi-phone"></i> {{ $rec->user->phone }}
                            @endif
                        </div>
                    </td>
                    <td>
                        <div class="fw-semibold text-dark">{{ $rec->book->title }}</div>
                        <div class="text-muted" style="font-size: 0.75rem;">
                            ISBN: {{ $rec->book->isbn }} • <span class="badge bg-light text-dark border">{{ $rec->book->category->name }}</span>
                        </div>
                    </td>
                    <td>{{ $rec->issue_date->format('d M Y') }}</td>
                    <td>
                        <span class="{{ $rec->status === 'overdue' ? 'text-danger fw-bold' : '' }}">
                            {{ $rec->due_date->format('d M Y') }}
                        </span>
                    </td>
                    <td>
                        @if($rec->return_date)
                            <span class="text-success"><i class="bi bi-check2"></i> {{ $rec->return_date->format('d M Y') }}</span>
                        @else
                            <span class="text-muted italic">— In Circulation —</span>
                        @endif
                    </td>
                    <td>
                        @if($rec->status === 'returned')
                            <span class="badge bg-success-subtle text-success border border-success-subtle">
                                Returned
                            </span>
                            @if($rec->fine_amount > 0)
                                <div class="text-danger small mt-1 fw-semibold">Paid Fine: ₹{{ number_format($rec->fine_amount, 2) }}</div>
                            @endif
                        @elseif($rec->status === 'overdue')
                            <span class="badge bg-danger text-white">
                                <i class="bi bi-exclamation-triangle-fill me-1"></i> Overdue
                            </span>
                            @if($rec->fine_amount > 0)
                                <div class="text-danger small mt-1 fw-bold">Due Fine: ₹{{ number_format($rec->fine_amount, 2) }}</div>
                            @endif
                        @else
                            <span class="badge bg-warning-subtle text-warning border border-warning-subtle">
                                Active Loan
                            </span>
                        @endif
                    </td>
                    <td class="text-end">
                        <div class="btn-group btn-group-sm">
                            @if($rec->status !== 'returned')
                            <button type="button" class="btn btn-outline-success" data-bs-toggle="modal" data-bs-target="#returnModal{{ $rec->id }}" title="Process Book Return">
                                <i class="bi bi-box-arrow-in-left me-1"></i> Return
                            </button>
                            @endif

                            <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delLoanModal{{ $rec->id }}" title="Delete Record">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>

                        <!-- Return Processing Modal -->
                        @if($rec->status !== 'returned')
                        <div class="modal fade" id="returnModal{{ $rec->id }}" tabindex="-1" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered text-start">
                                <div class="modal-content border-0 shadow">
                                    <form method="POST" action="{{ route('borrowings.return', $rec) }}">
                                        @csrf
                                        <div class="modal-header bg-success text-white">
                                            <h6 class="modal-title fw-bold"><i class="bi bi-box-arrow-in-left me-2"></i> Receive & Return Book</h6>
                                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body p-4">
                                            <p class="mb-2">Confirm return of book to library inventory:</p>
                                            <div class="p-3 bg-light rounded border mb-3">
                                                <div class="fw-bold">{{ $rec->book->title }}</div>
                                                <div class="text-muted small">Borrower: {{ $rec->user->name }}</div>
                                                <div class="text-muted small">Due Date: {{ $rec->due_date->format('d M Y') }}</div>
                                            </div>

                                            @if($rec->status === 'overdue' || \Carbon\Carbon::today()->gt($rec->due_date))
                                                @php
                                                    $daysLate = \Carbon\Carbon::today()->diffInDays($rec->due_date);
                                                    $estFine = $daysLate * 10;
                                                @endphp
                                                <div class="alert alert-danger py-2 px-3 small">
                                                    <i class="bi bi-exclamation-octagon-fill me-1"></i>
                                                    This book is <strong>{{ $daysLate }} days overdue</strong>. An automated late fee of <strong>₹{{ number_format($estFine, 2) }}</strong> (₹10/day) will be calculated.
                                                </div>
                                            @else
                                                <div class="alert alert-success py-2 px-3 small">
                                                    <i class="bi bi-check-circle-fill me-1"></i>
                                                    Returning on or before due date. No late fine applicable!
                                                </div>
                                            @endif

                                            <div class="mb-3">
                                                <label class="form-label fw-semibold small">Return Inspection Remarks (Optional)</label>
                                                <input type="text" name="remarks" class="form-control form-control-sm" placeholder="e.g. Returned in good condition" value="{{ $rec->remarks }}">
                                            </div>
                                        </div>
                                        <div class="modal-footer bg-light">
                                            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
                                            <button type="submit" class="btn btn-success btn-sm">Confirm Return & Restock</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                        @endif

                        <!-- Delete Loan Modal -->
                        <div class="modal fade" id="delLoanModal{{ $rec->id }}" tabindex="-1" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered text-start">
                                <div class="modal-content border-0 shadow">
                                    <div class="modal-header bg-danger text-white">
                                        <h6 class="modal-title fw-bold"><i class="bi bi-trash-fill me-2"></i> Delete Loan Record</h6>
                                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body p-4">
                                        <p class="mb-0">Are you sure you want to delete this borrowing transaction?</p>
                                        <div class="text-muted small mt-2">If active, the book's available stock will be restored automatically.</div>
                                    </div>
                                    <div class="modal-footer bg-light">
                                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
                                        <form method="POST" action="{{ route('borrowings.destroy', $rec) }}" class="d-inline">
                                            @csrf
                                            @method('DELETE')
                                            <button type="submit" class="btn btn-danger btn-sm">Delete Record</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                @empty
                <tr>
                    <td colspan="8" class="text-center py-5 text-muted">
                        <i class="bi bi-inbox fs-1 d-block mb-2 text-secondary"></i>
                        <h5>No loan records found</h5>
                        <p class="small mb-3">No active or historical loans match your current filter.</p>
                        <a href="{{ route('borrowings.create') }}" class="btn btn-primary btn-sm">Issue Book to Member</a>
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>

    @if($records->hasPages())
    <div class="card-footer bg-white border-top py-3">
        <div class="d-flex justify-content-between align-items-center">
            <span class="small text-muted">Showing {{ $records->firstItem() }} to {{ $records->lastItem() }} of {{ $records->total() }} records</span>
            <div>{{ $records->links('pagination::bootstrap-5') }}</div>
        </div>
    </div>
    @endif
</div>
@endsection
