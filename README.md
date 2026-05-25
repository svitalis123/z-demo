# Classroom Feedback Demo

A Django + DRF application demonstrating JWT authentication
and role-based access control with three roles:
Instructor, Student, and Observer.

## Local Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations and seed data:
   ```bash
   python manage.py migrate
   python manage.py seed
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

## Demo Accounts

| Role       | Email                | Password  |
|------------|----------------------|-----------|
| Instructor | instructor@demo.dev  | Demo@1234 |
| Student    | student@demo.dev     | Demo@1234 |
| Observer   | observer@demo.dev    | Demo@1234 |

## API Endpoints

- `POST /api/v1/auth/login/` — get access + refresh tokens
- `POST /api/v1/auth/refresh/` — refresh access token
- `GET /api/v1/assignments/` — list (role-filtered)
- `POST /api/v1/assignments/` — create (Instructor only)
- `POST /api/v1/submissions/` — submit (Student only)
- `GET /api/v1/submissions/{id}/feedback/` — view feedback

## Teaching Comment

Located in `classroom/permissions.py` — explains the
difference between `has_permission` and
`has_object_permission` and why row-level checks matter.

## How to Break This App

**1. No token blacklisting.** If an Instructor changes a
Student's role to Observer, the Student's existing JWT
still contains `"role": "STUDENT"` until it expires
(15 minutes). During that window, they retain Student
privileges. **Fix:** Use SimpleJWT's token blacklist app
to invalidate tokens on role change.

**2. No rate limiting on login.** An attacker can send
unlimited POST requests to `/api/v1/auth/login/` to
brute-force passwords. **Fix:** Add `django-ratelimit`
or `django-axes` to throttle failed login attempts
(e.g., 5 attempts per minute per IP).

---
