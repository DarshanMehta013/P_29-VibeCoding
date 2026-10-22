@extends('layouts.app')

@section('title', 'Add New Book')

@section('content')
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center justify-content-between mb-3">
            <div>
                <h4 class="fw-bold mb-1 text-dark"><i class="bi bi-plus-circle text-primary me-2"></i> Add New Book to Catalog</h4>
                <p class="text-muted small mb-0">Enter the bibliographic and inventory details of the new acquisition.</p>
            </div>
            <a href="{{ route('books.index') }}" class="btn btn-outline-secondary btn-sm">
                <i class="bi bi-arrow-left me-1"></i> Back to Catalog
            </a>
        </div>

        <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
                <form method="POST" action="{{ route('books.store') }}">
                    @csrf

                    <div class="row g-3">
                        <!-- Book Title -->
                        <div class="col-12">
                            <label for="title" class="form-label fw-semibold small">Book Title *</label>
                            <input type="text" class="form-control @error('title') is-invalid @enderror" id="title" name="title" value="{{ old('title') }}" placeholder="e.g. Clean Code: A Handbook of Agile Software Craftsmanship" required>
                            @error('title')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- Author & Category -->
                        <div class="col-md-6">
                            <label for="author" class="form-label fw-semibold small">Author(s) *</label>
                            <input type="text" class="form-control @error('author') is-invalid @enderror" id="author" name="author" value="{{ old('author') }}" placeholder="e.g. Robert C. Martin" required>
                            @error('author')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="col-md-6">
                            <label for="category_id" class="form-label fw-semibold small">Category / Discipline *</label>
                            <select class="form-select @error('category_id') is-invalid @enderror" id="category_id" name="category_id" required>
                                <option value="">-- Select Category --</option>
                                @foreach($categories as $cat)
                                    <option value="{{ $cat->id }}" {{ old('category_id') == $cat->id ? 'selected' : '' }}>
                                        {{ $cat->name }} ({{ $cat->code }})
                                    </option>
                                @endforeach
                            </select>
                            @error('category_id')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- ISBN & Publisher -->
                        <div class="col-md-6">
                            <label for="isbn" class="form-label fw-semibold small">ISBN Number * (Unique)</label>
                            <input type="text" class="form-control font-monospace @error('isbn') is-invalid @enderror" id="isbn" name="isbn" value="{{ old('isbn') }}" placeholder="e.g. 978-0132350884" required>
                            @error('isbn')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="col-md-6">
                            <label for="publisher" class="form-label fw-semibold small">Publisher</label>
                            <input type="text" class="form-control @error('publisher') is-invalid @enderror" id="publisher" name="publisher" value="{{ old('publisher') }}" placeholder="e.g. Prentice Hall">
                            @error('publisher')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- Publication Year, Copies, Rack -->
                        <div class="col-md-4">
                            <label for="publication_year" class="form-label fw-semibold small">Publication Year</label>
                            <input type="number" class="form-control @error('publication_year') is-invalid @enderror" id="publication_year" name="publication_year" value="{{ old('publication_year', date('Y')) }}" min="1900" max="{{ date('Y') + 1 }}">
                            @error('publication_year')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="col-md-4">
                            <label for="total_copies" class="form-label fw-semibold small">Total Copies in Stock *</label>
                            <input type="number" class="form-control @error('total_copies') is-invalid @enderror" id="total_copies" name="total_copies" value="{{ old('total_copies', 1) }}" min="1" max="999" required>
                            @error('total_copies')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="col-md-4">
                            <label for="rack_location" class="form-label fw-semibold small">Rack / Shelf Location</label>
                            <input type="text" class="form-control @error('rack_location') is-invalid @enderror" id="rack_location" name="rack_location" value="{{ old('rack_location', 'Rack A-01') }}" placeholder="e.g. Rack A-01">
                            @error('rack_location')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- Description -->
                        <div class="col-12">
                            <label for="description" class="form-label fw-semibold small">Book Synopsis / Abstract</label>
                            <textarea class="form-control @error('description') is-invalid @enderror" id="description" name="description" rows="3" placeholder="Brief summary of book contents, edition details, and topics covered...">{{ old('description') }}</textarea>
                            @error('description')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="col-12 pt-3 border-top d-flex gap-2">
                            <button type="submit" class="btn btn-primary px-4 fw-semibold">
                                <i class="bi bi-save me-1"></i> Save to Catalog
                            </button>
                            <a href="{{ route('books.index') }}" class="btn btn-light border px-3">
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
