FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt
COPY backend/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY backend/ .

# Запускаем приложение
CMD ["python", "run.py"]
