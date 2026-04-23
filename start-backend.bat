@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

echo.
echo ======================================
echo  AcademiaSphere Backend Server Startup
echo ======================================
echo.

if not exist "%PYTHON_EXE%" (
    echo [1/3] Creating project virtual environment in .venv...
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
    pause
    exit /b 1
)

echo [1/3] Using Python:
"%PYTHON_EXE%" --version

echo.
echo [2/3] Checking backend dependencies...
"%PYTHON_EXE%" -c "import flask, flask_cors, psycopg2, joblib, pandas, sklearn" >nul 2>&1
if errorlevel 1 (
    echo Installing requirements into .venv...
    "%PYTHON_EXE%" -m pip install -r "%ROOT_DIR%Backend\requirements.txt"
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed.
        echo Try rerunning this script after confirming internet access.
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed.
)

echo.
echo [3/3] Starting Flask server...
echo.
echo Backend URL: http://127.0.0.1:5000
echo If PostgreSQL is not ready yet, review Backend\app.py and Backend\database.py.
echo Press Ctrl+C to stop the server.
echo.

pushd "%ROOT_DIR%Backend"
"%PYTHON_EXE%" app.py
popd

pause
endlocal
