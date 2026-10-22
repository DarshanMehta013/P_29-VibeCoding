@extends('layouts.app')

@section('title', 'Staff & Member Login')

@section('content')
<div class="row justify-content-center py-4">
    <div class="col-md-5 col-lg-4">
        <div class="card shadow-sm border-0">
            <div class="card-body p-4 p-md-5">
                <div class="text-center mb-4">
                    <div class="badge bg-primary rounded-circle p-3 mb-3">
                        <i class="bi bi-shield-lock-fill fs-3 text-white"></i>
                    </div>
                    <h4 class="fw-bold mb-1">User Sign In</h4>
                    <p class="text-muted small">Access the Library Management System portal</p>
                </div>

                <!-- Quick Test Credentials Box -->
                <div class="alert alert-light border small mb-4 py-2 px-3">
                    <strong class="d-block text-primary mb-1"><i class="bi bi-key-fill me-1"></i> Demo Credentials:</strong>
                    <div class="text-muted">Email: <code>admin@librasys.test</code></div>
                    <div class="text-muted">Password: <code>password123</code></div>
                </div>

                <form method="POST" action="{{ route('login.post') }}">
                    @csrf
                    <div class="mb-3">
                        <label for="email" class="form-label fw-semibold small">Email Address</label>
                        <div class="input-group">
                            <span class="input-group-text bg-light"><i class="bi bi-envelope"></i></span>
                            <input type="email" class="form-control @error('email') is-invalid @enderror" id="email" name="email" value="{{ old('email', 'admin@librasys.test') }}" required autofocus>
                        </div>
                        @error('email')
                            <div class="invalid-feedback d-block">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label fw-semibold small">Password</label>
                        <div class="input-group">
                            <span class="input-group-text bg-light"><i class="bi bi-lock"></i></span>
                            <input type="password" class="form-control @error('password') is-invalid @enderror" id="password" name="password" value="password123" required>
                        </div>
                        @error('password')
                            <div class="invalid-feedback d-block">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="mb-4 form-check">
                        <input type="checkbox" class="form-check-input" id="remember" name="remember">
                        <label class="form-check-label small text-muted" for="remember">Keep me logged in on this device</label>
                    </div>

                    <button type="submit" class="btn btn-primary w-100 py-2 fw-semibold">
                        <i class="bi bi-box-arrow-in-right me-1"></i> Sign In to Account
                    </button>
                </form>

                <div class="text-center mt-4 pt-2 border-top">
                    <span class="text-muted small">New to the library?</span>
                    <a href="{{ route('register') }}" class="small fw-semibold text-decoration-none ms-1">Create Account</a>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
