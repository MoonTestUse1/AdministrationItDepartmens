#!/bin/bash

# Ждем, пока база данных будет доступна
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Database is ready!"

# Устанавливаем переменные окружения
export PYTHONPATH=/app
export DATABASE_URL="postgresql://postgres:postgres123@db:5432/support_db"

# Применяем миграции
echo "Applying database migrations..."
cd /app
alembic upgrade head

# Проверяем, что миграции применились успешно
if [ $? -eq 0 ]; then
    echo "Migrations completed successfully!"
else
    echo "Error applying migrations!"
    exit 1
fi

# Запускаем приложение
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --workers 1 