@echo off
REM DataZen Analytics - Windows Setup Script

echo ===============================================
echo DataZen Analytics - Django Website Setup
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Running database migrations...
python datazen_website\manage.py migrate
if errorlevel 1 (
    echo Error: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo Next steps:
echo   1. Create superuser: python datazen_website\manage.py createsuperuser
echo   2. Run server: python datazen_website\manage.py runserver
echo   3. Open: http://127.0.0.1:8000/
echo   4. Admin: http://127.0.0.1:8000/admin/
echo.
pause
