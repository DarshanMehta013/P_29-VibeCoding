@extends('layouts.app')

@section('title', 'Executive Reports & Analytics Summary')

@section('styles')
<style>
@media print {
    nav, footer, .btn-print, .alert {
        display: none !important;
    }
    body {
        background-color: #ffffff !important;
    }
    .card {
        box-shadow: none !important;
        border: 1px solid #ddd !important;
    }
}
</style>
@endsection

@section('content')
<div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
    <div>
        <h4 class="fw-bold mb-1 text-dark"><i class="bi bi-bar-chart-line text-primary me-2"></i> Library Circulation & Inventory Audit Report</h4>
        <p class="text-muted small mb-0">Database aggregation and inventory analysis generated on {{ date('d M Y, h:i A') }}</p>
    </div>
    <div>
        <button type="button" class="btn btn-outline-secondary btn-print fw-semibold" onclick="window.print()">
            <i class="bi bi-printer me-1"></i> Print / Save PDF
        </button>
    </div>
</div>

<!-- 1. Executive Summary Metric Badges -->
<div class="card border-0 shadow-sm mb-4">
    <div class="card-header bg-white border-bottom py-3">
        <h6 class="fw-bold mb-0 text-dark"><i class="bi bi-clipboard-data text-primary me-2"></i> Section A: High-Level Inventory Metrics</h6>
    </div>
    <div class="card-body p-4">
        <div class="row g-3 text-center">
            <div class="col-6 col-md-3 border-end">
                <div class="text-muted small mb-1">Total Catalog Titles</div>
                <h3 class="fw-bold text-dark mb-0">{{ $summary['total_books'] }}</h3>
                <small class="text-muted">Unique ISBNs</small>
            </div>
            <div class="col-6 col-md-3 border-end">
                <div class="text-muted small mb-1">Total Stock Volumes</div>
                <h3 class="fw-bold text-primary mb-0">{{ $summary['total_copies'] }}</h3>
                <small class="text-muted">{{ $summary['available_copies'] }} on shelf ({{ round(($summary['available_copies'] / max($summary['total_copies'], 1)) * 100, 1) }}%)</small>
            </div>
            <div class="col-6 col-md-3 border-end">
                <div class="text-muted small mb-1">Books in Circulation</div>
                <h3 class="fw-bold text-warning mb-0">{{ $summary['borrowed_copies'] }}</h3>
                <small class="text-muted">{{ $summary['active_loans'] }} active transactions</small>
            </div>
            <div class="col-6 col-md-3">
                <div class="text-muted small mb-1">Overdue Loans & Penalties</div>
                <h3 class="fw-bold text-danger mb-0">{{ $summary['overdue_loans'] }}</h3>
                <small class="text-danger fw-semibold">₹{{ number_format($summary['total_fines'], 2) }} assessed</small>
            </div>
        </div>
    </div>
</div>

<!-- 2. Category Distribution & Stock Utilization Breakdown -->
<div class="card border-0 shadow-sm mb-4">
    <div class="card-header bg-white border-bottom py-3">
        <h6 class="fw-bold mb-0 text-dark"><i class="bi bi-pie-chart text-primary me-2"></i> Section B: Category & Departmental Utilization Breakdown</h6>
    </div>
    <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small">
            <thead class="table-light">
                <tr>
                    <th>Department / Category</th>
                    <th>Code</th>
                    <th>Unique Titles</th>
                    <th>Total Volumes</th>
                    <th>In Circulation</th>
                    <th>Available Stock</th>
                    <th style="width: 200px;">Utilization Rate</th>
                </tr>
            </thead>
            <tbody>
                @foreach($categoriesReport as $cat)
                <tr>
                    <td class="fw-bold text-dark">{{ $cat->name }}</td>
                    <td><span class="badge bg-light text-primary border font-monospace">{{ $cat->code }}</span></td>
                    <td>{{ $cat->titles_count }}</td>
                    <td>{{ $cat->total_copies }}</td>
                    <td class="text-warning fw-semibold">{{ $cat->borrowed_copies }}</td>
                    <td class="text-success fw-semibold">{{ $cat->available_copies }}</td>
                    <td>
                        <div class="d-flex align-items-center gap-2">
                            <div class="progress flex-grow-1" style="height: 6px;">
                                <div class="progress-bar bg-primary" role="progressbar" style="width: {{ $cat->utilization_rate }}%;" aria-valuenow="{{ $cat->utilization_rate }}" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                            <span class="text-muted small">{{ $cat->utilization_rate }}%</span>
                        </div>
                    </td>
                </tr>
                @endforeach
            </tbody>
        </table>
    </div>
</div>

<!-- 3. Overdue & Critical Delinquent Loans Report -->
<div class="card border-0 shadow-sm">
    <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
        <h6 class="fw-bold mb-0 text-danger"><i class="bi bi-exclamation-octagon-fill me-2"></i> Section C: Critical Overdue Loans & Penalties Audit</h6>
        <span class="badge bg-danger text-white">{{ count($overdueRecords) }} Delinquent Loans</span>
    </div>
    <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small">
            <thead class="table-light">
                <tr>
                    <th style="width: 50px;">#</th>
                    <th>Member / Student Name</th>
                    <th>Book Title</th>
                    <th>ISBN</th>
                    <th>Original Due Date</th>
                    <th>Days Overdue</th>
                    <th>Assessed Fine (₹10/day)</th>
                </tr>
            </thead>
            <tbody>
                @forelse($overdueRecords as $overdue)
                <tr>
                    <td class="text-muted">{{ $overdue->id }}</td>
                    <td>
                        <div class="fw-bold text-dark">{{ $overdue->member_name }}</div>
                        <div class="text-muted" style="font-size: 0.75rem;">{{ $overdue->member_email }}</div>
                    </td>
                    <td>
                        <div class="fw-semibold text-dark">{{ $overdue->book_title }}</div>
                    </td>
                    <td class="font-monospace text-muted">{{ $overdue->isbn }}</td>
                    <td class="text-danger fw-semibold">{{ $overdue->due_date }}</td>
                    <td>
                        <span class="badge bg-danger-subtle text-danger border border-danger-subtle">
                            {{ $overdue->days_late }} Days Late
                        </span>
                    </td>
                    <td class="fw-bold text-danger">₹{{ number_format($overdue->fine, 2) }}</td>
                </tr>
                @empty
                <tr>
                    <td colspan="7" class="text-center py-4 text-success">
                        <i class="bi bi-check-circle-fill me-1"></i> No overdue loans! All issued books are within their due return periods.
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>
@endsection
