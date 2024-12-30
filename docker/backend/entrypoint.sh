#!/bin/sh
set -e

# Run database initialization
python /app/scripts/init_db.py

# Start the main application
exec python /app/run.py