# AcademiaSphere Default Login Credentials

## Quick Reference

| Role | Username | Password | Dashboard |
|------|----------|----------|-----------|
| Admin | `admin` | `admin123` | `admin-dashboard.html` |
| Teacher | `teacher` | `teacher123` | `teacher-dashboard.html` |
| Parent | `parent` | `parent123` | `parent-dashboard.html` |

## Quick Start

1. Start PostgreSQL.
2. Run `start-backend.bat`.
3. Wait for the Flask server to start on `http://127.0.0.1:5000`.
4. Open `frontend/login.html`.
5. Sign in with one of the accounts above.

## Backend URLs

The frontend uses the saved API base from login and defaults to:

- `http://127.0.0.1:5000/api`

The login page can also try:

- `http://localhost:5000/api`
- `http://127.0.0.1:5001/api`
- `http://localhost:5001/api`

## Not Working?

1. Run `verify-setup.bat`.
2. Confirm PostgreSQL is running and the credentials in `Backend/app.py` match your machine.
3. Confirm the backend window shows `http://127.0.0.1:5000`.
4. Check the browser console for API or CORS errors.

See `LOGIN_SETUP_GUIDE.md` and `TROUBLESHOOTING.md` for more detail.
