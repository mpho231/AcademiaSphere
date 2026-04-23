# AcademiaSphere

AcademiaSphere is a school management prototype with:

- a Flask backend in `Backend/`
- the active browser UI in `frontend/`
- an ML risk model used for at-risk student predictions
- PostgreSQL as the current database backend

## Quick Start

1. Make sure PostgreSQL is running.
2. Review the database credentials in `Backend/app.py` and `Backend/database.py`.
3. Run `start-backend.bat`.
4. Open `frontend/login.html` in your browser.

The startup script uses the project `.venv` automatically and installs missing Python packages into it.

## Default Accounts

- Admin: `admin` / `admin123`
- Teacher: `teacher` / `teacher123`
- Parent: `parent` / `parent123`

## Useful Commands

- Start backend: `start-backend.bat`
- Verify local setup: `verify-setup.bat`
- Create database if needed: `.venv\Scripts\python.exe Backend\database.py`
- Train the ML model: `.venv\Scripts\python.exe Backend\ml_model.py`

## Project Layout

- `Backend/` Flask API, database setup, ML inference
- `frontend/` login page and role dashboards
- `report/` project writeups

## Notes

- The current codebase expects PostgreSQL, not MySQL.
- The login page and dashboards use the API base saved at sign-in, with `http://127.0.0.1:5000/api` as the default.
- If your PostgreSQL username or password is different, update both `Backend/app.py` and `Backend/database.py`.
