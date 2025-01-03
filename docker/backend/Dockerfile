FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY backend/ .

# Создаем entrypoint скрипт
RUN echo '#!/bin/sh\n\
echo "Waiting for database..."\n\
sleep 5\n\
echo "Running database migrations..."\n\
alembic upgrade head\n\
echo "Starting application..."\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]