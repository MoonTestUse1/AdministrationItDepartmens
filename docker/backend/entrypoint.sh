#!/bin/sh
set -e

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Run database migrations
echo "Running database migrations..."
cd /app && alembic upgrade head

# Run database initialization
echo "Initializing database..."
python /app/scripts/init_db.py

# Start the main application
echo "Starting application..."
exec python /app/run.py