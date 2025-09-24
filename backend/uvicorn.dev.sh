#!/bin/bash

# Development server startup script
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the development server
echo "Starting development server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
