@extends('layouts.app')

@section('title', 'Member Registration')

@section('content')
<div class="row justify-content-center py-4">
    <div class="col-md-6 col-lg-5">
        <div class="card shadow-sm border-0">
            <div class="card-body p-4 p-md-5">
                <div class="text-center mb-4">
                    <div class="badge bg-primary rounded-circle p-3 mb-3">
                        <i class="bi bi-person-plus-fill fs-3 text-white"></i>
                    </div>
                    <h4 class="fw-bold mb-1">Create Library Account</h4>
                    <p class="text-muted small">Register as a student or staff library member</p>
                </div>

                <form method="POST" action="{{ route('register.post') }}">
                    @csrf
                    <div class="mb-3">
                        <label for="name" class="form-label fw-semibold small">Full Name *</label>
                        <input type="text" class="form-control @error('name') is-invalid @enderror" id="name" name="name" value="{{ old('name') }}" placeholder="e.g. Darshan Mehta" required autofocus>
                        @error('name')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label fw-semibold small">Email Address *</label>
                        <input type="email" class="form-control @error('email') is-invalid @enderror" id="email" name="email" value="{{ old('email') }}" placeholder="e.g. darshan@example.com" required>
                        @error('email')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="mb-3">
                        <label for="phone" class="form-label fw-semibold small">Mobile Phone (Optional)</label>
                        <input type="text" class="form-control @error('phone') is-invalid @enderror" id="phone" name="phone" value="{{ old('phone') }}" placeholder="e.g. 9876543210">
                        @error('phone')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="password" class="form-label fw-semibold small">Password *</label>
                            <input type="password" class="form-control @error('password') is-invalid @enderror" id="password" name="password" placeholder="At least 6 chars" required>
                            @error('password')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>
                        <div class="col-md-6 mb-4">
                            <label for="password_confirmation" class="form-label fw-semibold small">Confirm Password *</label>
                            <input type="password" class="form-control" id="password_confirmation" name="password_confirmation" placeholder="Repeat password" required>
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary w-100 py-2 fw-semibold">
                        <i class="bi bi-check2-circle me-1"></i> Complete Registration
                    </button>
                </form>

                <div class="text-center mt-4 pt-2 border-top">
                    <span class="text-muted small">Already have an account?</span>
                    <a href="{{ route('login') }}" class="small fw-semibold text-decoration-none ms-1">Sign In</a>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
