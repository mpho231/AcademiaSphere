# Troubleshooting: Cannot Connect to Server

Use this checklist for the current PostgreSQL-based setup.

## Quick Check

1. Run `verify-setup.bat`.
2. Start the backend with `start-backend.bat`.
3. Open `frontend/login.html`.
4. Sign in with:
   - `admin` / `admin123`
   - `teacher` / `teacher123`
   - `parent` / `parent123`

## If the Backend Does Not Start

Check these first:

- `.venv` exists or can be created
- PostgreSQL is running
- `Backend/app.py` and `Backend/database.py` use the correct username and password
- port `5000` is available

## If Dependency Installation Fails

Run:

```bat
.venv\Scripts\python.exe -m pip install -r Backend\requirements.txt
```

If that fails, confirm internet access and that Python packaging tools are allowed to download dependencies.

## If PostgreSQL Fails

1. Confirm the server is running.
2. Confirm port `5432` is open locally.
3. Confirm the configured user can connect.
4. If the `academiasphere` database is missing, run:

```bat
.venv\Scripts\python.exe Backend\database.py
```

## If Login Fails

1. Make sure the backend is running.
2. Confirm the selected role matches the username.
3. Clear stale browser storage if you changed environments:

```js
localStorage.removeItem('academiasphere_user');
localStorage.removeItem('academiasphere_api_base');
```

4. Retry login from `frontend/login.html`.

## If Dashboards Load But API Calls Fail

The dashboards reuse the API base saved at login. If that saved value is wrong:

1. Sign out.
2. Clear `academiasphere_api_base` from local storage.
3. Sign in again.

## Useful Checks

- Backend health: `http://127.0.0.1:5000/api/test-db`
- Login endpoint: `http://127.0.0.1:5000/api/login`
- Setup script: `verify-setup.bat`
