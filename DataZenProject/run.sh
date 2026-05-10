#!/bin/bash
# DataZen Analytics - Quick Run Script

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

source venv/bin/activate
python datazen_website/manage.py runserver
