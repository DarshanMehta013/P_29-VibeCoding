@extends('layouts.app')

@section('title', 'Manage Book Categories')

@section('content')
<div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
    <div>
        <h4 class="fw-bold mb-1 text-dark"><i class="bi bi-tags text-primary me-2"></i> Book Categories & Disciplines</h4>
        <p class="text-muted small mb-0">Organize library catalog by departments, genres, and classification codes.</p>
    </div>
    <div>
        <button type="button" class="btn btn-primary px-3 shadow-sm fw-semibold" data-bs-toggle="modal" data-bs-target="#addCategoryModal">
            <i class="bi bi-plus-lg me-1"></i> New Category
        </button>
    </div>
</div>

<div class="row g-4">
    <div class="col-12">
        <div class="card border-0 shadow-sm">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light small">
                        <tr>
                            <th style="width: 60px;">#</th>
                            <th>Category Name</th>
                            <th>Code</th>
                            <th>Description</th>
                            <th>Cataloged Titles</th>
                            <th class="text-end" style="width: 140px;">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="small">
                        @forelse($categories as $cat)
                        <tr>
                            <td class="text-muted">{{ $cat->id }}</td>
                            <td>
                                <div class="fw-bold text-dark">{{ $cat->name }}</div>
                            </td>
                            <td>
                                <span class="badge bg-light text-primary border font-monospace">{{ $cat->code }}</span>
                            </td>
                            <td class="text-muted">{{ $cat->description ?? '— No description —' }}</td>
                            <td>
                                <span class="badge bg-primary-subtle text-primary border border-primary-subtle">
                                    {{ $cat->books_count }} titles
                                </span>
                            </td>
                            <td class="text-end">
                                <div class="btn-group btn-group-sm">
                                    <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#editModal{{ $cat->id }}" title="Edit Category">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delModal{{ $cat->id }}" title="Delete Category">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>

                                <!-- Edit Category Modal -->
                                <div class="modal fade" id="editModal{{ $cat->id }}" tabindex="-1" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered text-start">
                                        <div class="modal-content border-0 shadow">
                                            <form method="POST" action="{{ route('categories.update', $cat) }}">
                                                @csrf
                                                @method('PUT')
                                                <div class="modal-header bg-primary text-white">
                                                    <h6 class="modal-title fw-bold"><i class="bi bi-pencil-square me-2"></i> Edit Category</h6>
                                                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div class="modal-body p-4">
                                                    <div class="mb-3">
                                                        <label class="form-label fw-semibold small">Category Name *</label>
                                                        <input type="text" name="name" class="form-control" value="{{ $cat->name }}" required>
                                                    </div>
                                                    <div class="mb-3">
                                                        <label class="form-label fw-semibold small">Department Code *</label>
                                                        <input type="text" name="code" class="form-control font-monospace" value="{{ $cat->code }}" required>
                                                    </div>
                                                    <div class="mb-3">
                                                        <label class="form-label fw-semibold small">Description</label>
                                                        <textarea name="description" class="form-control" rows="3">{{ $cat->description }}</textarea>
                                                    </div>
                                                </div>
                                                <div class="modal-footer bg-light">
                                                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
                                                    <button type="submit" class="btn btn-primary btn-sm">Save Changes</button>
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                                </div>

                                <!-- Delete Modal -->
                                <div class="modal fade" id="delModal{{ $cat->id }}" tabindex="-1" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered text-start">
                                        <div class="modal-content border-0 shadow">
                                            <div class="modal-header bg-danger text-white">
                                                <h6 class="modal-title fw-bold"><i class="bi bi-trash-fill me-2"></i> Delete Category</h6>
                                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body p-4">
                                                <p class="mb-2">Are you sure you want to delete category <strong>{{ $cat->name }}</strong>?</p>
                                                <small class="text-muted">Categories with active book titles cannot be deleted until all books are reassigned or removed.</small>
                                            </div>
                                            <div class="modal-footer bg-light">
                                                <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
                                                <form method="POST" action="{{ route('categories.destroy', $cat) }}" class="d-inline">
                                                    @csrf
                                                    @method('DELETE')
                                                    <button type="submit" class="btn btn-danger btn-sm">Confirm Delete</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                        @empty
                        <tr>
                            <td colspan="6" class="text-center py-4 text-muted">No categories configured yet.</td>
                        </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<!-- Add Category Modal -->
<div class="modal fade" id="addCategoryModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
            <form method="POST" action="{{ route('categories.store') }}">
                @csrf
                <div class="modal-header bg-primary text-white">
                    <h6 class="modal-title fw-bold"><i class="bi bi-plus-circle me-2"></i> Create New Book Category</h6>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4">
                    <div class="mb-3">
                        <label for="new_cat_name" class="form-label fw-semibold small">Category Name *</label>
                        <input type="text" id="new_cat_name" name="name" class="form-control" placeholder="e.g. Artificial Intelligence" required>
                    </div>
                    <div class="mb-3">
                        <label for="new_cat_code" class="form-label fw-semibold small">Short Code *</label>
                        <input type="text" id="new_cat_code" name="code" class="form-control font-monospace" placeholder="e.g. AI-DEPT" required>
                    </div>
                    <div class="mb-3">
                        <label for="new_cat_desc" class="form-label fw-semibold small">Description</label>
                        <textarea id="new_cat_desc" name="description" class="form-control" rows="3" placeholder="Scope and subject matter of this classification..."></textarea>
                    </div>
                </div>
                <div class="modal-footer bg-light">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary btn-sm">Create Category</button>
                </div>
            </form>
        </div>
    </div>
</div>
@endsection
