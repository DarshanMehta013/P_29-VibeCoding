@extends('layouts.app')

@section('title', 'Issue Book to Member')

@section('content')
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center justify-content-between mb-3">
            <div>
                <h4 class="fw-bold mb-1 text-dark"><i class="bi bi-journal-arrow-up text-primary me-2"></i> Issue Book to Member</h4>
                <p class="text-muted small mb-0">Record a new book loan and allocate physical volume to a registered member.</p>
            </div>
            <a href="{{ route('borrowings.index') }}" class="btn btn-outline-secondary btn-sm">
                <i class="bi bi-arrow-left me-1"></i> Back to Loan Records
            </a>
        </div>

        <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
                <form method="POST" action="{{ route('borrowings.store') }}">
                    @csrf

                    <div class="row g-3">
                        <!-- Select Member -->
                        <div class="col-md-6">
                            <label for="user_id" class="form-label fw-semibold small">Select Student / Member *</label>
                            <select class="form-select @error('user_id') is-invalid @enderror" id="user_id" name="user_id" required>
                                <option value="">-- Choose Member --</option>
                                @foreach($members as $m)
                                    <option value="{{ $m->id }}" {{ old('user_id') == $m->id ? 'selected' : '' }}>
                                        {{ $m->name }} ({{ $m->email }})
                                    </option>
                                @endforeach
                            </select>
                            @error('user_id')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- Select Book -->
                        <div class="col-md-6">
                            <label for="book_id" class="form-label fw-semibold small">Select Available Book *</label>
                            <select class="form-select @error('book_id') is-invalid @enderror" id="book_id" name="book_id" required>
                                <option value="">-- Choose Book in Stock --</option>
                                @foreach($availableBooks as $b)
                                    <option value="{{ $b->id }}" {{ (old('book_id', request('book_id')) == $b->id) ? 'selected' : '' }}>
                                        {{ $b->title }} ({{ $b->available_copies }} copies left)
                                    </option>
                                @endforeach
                            </select>
                            @error('book_id')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- Issue Date & Due Date -->
                        <div class="col-md-6">
                            <label for="issue_date" class="form-label fw-semibold small">Issue Date *</label>
                            <input type="date" class="form-control @error('issue_date') is-invalid @enderror" id="issue_date" name="issue_date" value="{{ old('issue_date', date('Y-m-d')) }}" required>
                            @error('issue_date')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="col-md-6">
                            <label for="due_date" class="form-label fw-semibold small">Due Return Date * (Standard 14 Days)</label>
                            <input type="date" class="form-control @error('due_date') is-invalid @enderror" id="due_date" name="due_date" value="{{ old('due_date', date('Y-m-d', strtotime('+14 days'))) }}" required>
                            @error('due_date')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- Remarks -->
                        <div class="col-12">
                            <label for="remarks" class="form-label fw-semibold small">Issuing Remarks / Condition Notes (Optional)</label>
                            <input type="text" class="form-control @error('remarks') is-invalid @enderror" id="remarks" name="remarks" value="{{ old('remarks') }}" placeholder="e.g. Issued for final semester project research">
                            @error('remarks')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="col-12 pt-3 border-top d-flex gap-2">
                            <button type="submit" class="btn btn-primary px-4 fw-semibold">
                                <i class="bi bi-check2-circle me-1"></i> Confirm & Issue Book
                            </button>
                            <a href="{{ route('borrowings.index') }}" class="btn btn-light border px-3">
                                Cancel
                            </a>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
@endsection
