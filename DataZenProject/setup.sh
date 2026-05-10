#!/bin/bash
# DataZen Analytics - Linux/macOS Setup Script

echo "========================================"
echo "DataZen Analytics - Django Website Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Running database migrations..."
python datazen_website/manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to run migrations"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Create superuser: python datazen_website/manage.py createsuperuser"
echo "  2. Run server: python datazen_website/manage.py runserver"
echo "  3. Open: http://127.0.0.1:8000/"
echo "  4. Admin: http://127.0.0.1:8000/admin/"
echo ""
