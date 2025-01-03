#!/bin/bash

# Ждем, пока база данных будет доступна
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Database is ready!"

# Применяем миграции
echo "Applying database migrations..."
cd /app
export DATABASE_URL="postgresql://postgres:postgres123@db:5432/support_db"
alembic upgrade head

echo "Migrations completed!"

# Запускаем приложение
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --workers 1 