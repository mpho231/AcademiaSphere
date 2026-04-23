# AcademiaSphere Login and Dashboard Guide

This guide matches the current codebase in this repository.

## Default Login Credentials

- Admin: `admin` / `admin123`
- Teacher: `teacher` / `teacher123`
- Parent: `parent` / `parent123`

## Current Stack

- Backend: Flask
- Database: PostgreSQL
- Frontend: static HTML dashboards in `frontend/`
- ML: scikit-learn model loaded from `Backend/model.pkl`

## Backend Setup

1. Make sure PostgreSQL is installed and running.
2. Review `DB_CONFIG` in both `Backend/app.py` and `Backend/database.py`.
3. Run `start-backend.bat`.

The startup script will:

- create `.venv` if it does not already exist
- install missing Python dependencies into `.venv`
- start the Flask app from `Backend/app.py`

## Database Setup

If the `academiasphere` database does not exist yet, run:

```bat
.venv\Scripts\python.exe Backend\database.py
```

That script creates the PostgreSQL database if needed and then lets the app initialize tables and seed data.

## Frontend Login Flow

1. Open `frontend/login.html`.
2. Enter a username, password, and role.
3. The login page sends a request to the Flask API and stores:
   - `academiasphere_user`
   - `academiasphere_api_base`
4. The user is redirected to the matching dashboard page.

## Dashboard Pages

- `frontend/admin-dashboard.html`
- `frontend/teacher-dashboard.html`
- `frontend/parent-dashboard.html`

These dashboards read the API base saved at login, so the same backend URL is reused after sign-in.

## Common Commands

```bat
start-backend.bat
verify-setup.bat
.venv\Scripts\python.exe Backend\database.py
.venv\Scripts\python.exe Backend\ml_model.py
```

## If Login Fails

1. Run `verify-setup.bat`.
2. Confirm PostgreSQL is reachable with the configured credentials.
3. Confirm the backend is running on `http://127.0.0.1:5000`.
4. Open the browser console and check the failing API URL.
5. Make sure the selected role matches the account:
   - `admin` -> Administrator
   - `teacher` -> Teacher
   - `parent` -> Parent

## Notes

- The older MySQL instructions no longer apply to this version of the project.
- The backend seeds one default teacher and one default parent account, not `teacher1`, `teacher2`, `parent1`, or `parent2`.
