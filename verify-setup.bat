@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

echo.
echo ======================================
echo  AcademiaSphere Setup Verification
echo ======================================
echo.

if not exist "%PYTHON_EXE%" (
    echo [1/4] Creating project virtual environment in .venv...
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3.14 -m venv "%VENV_DIR%" >nul 2>&1
        if errorlevel 1 (
            py -3 -m venv "%VENV_DIR%" >nul 2>&1
        )
    ) else (
        python -m venv "%VENV_DIR%" >nul 2>&1
    )
)

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python 3 was not found.
    echo Install Python, then rerun this script.
    goto :end
)

echo [1/4] Checking Python...
"%PYTHON_EXE%" --version
echo [OK] Python available in .venv

echo.
echo [2/4] Checking backend dependencies...
"%PYTHON_EXE%" -c "import flask, flask_cors, psycopg2, joblib, pandas, sklearn" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Missing packages detected. Installing requirements...
    "%PYTHON_EXE%" -m pip install -r "%ROOT_DIR%Backend\requirements.txt"
    if errorlevel 1 (
        echo [ERROR] Could not install required packages.
        goto :end
    )
) else (
    echo [OK] Required packages are installed
)

echo.
echo [3/4] Checking PostgreSQL connectivity...
"%PYTHON_EXE%" -c "import runpy, psycopg2; cfg = runpy.run_path(r'%ROOT_DIR%Backend\database.py')['DB_CONFIG']; psycopg2.connect(host=cfg['host'], port=cfg['port'], user=cfg['user'], password=cfg['password'], dbname='postgres').close()" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL is not reachable with the current settings.
    echo Review the DB_CONFIG values in Backend\app.py and Backend\database.py.
    goto :end
) else (
    echo [OK] PostgreSQL connection succeeded
)

echo.
echo [4/4] Checking backend HTTP endpoint...
"%PYTHON_EXE%" -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:5000/api/test-db', timeout=2)" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Backend is not responding on http://127.0.0.1:5000
    echo Start it with start-backend.bat, then rerun this script.
) else (
    echo [OK] Backend HTTP endpoint is responding
)

echo.
echo ======================================
echo         Verification Complete
echo ======================================
echo.

:end
pause
endlocal
