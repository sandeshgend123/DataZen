@echo off
REM DataZen Analytics - Quick Run Script

if not exist venv\ (
    echo Virtual environment not found. Please run setup.bat first.
    exit /b 1
)

call venv\Scripts\activate.bat
python datazen_website\manage.py runserver
