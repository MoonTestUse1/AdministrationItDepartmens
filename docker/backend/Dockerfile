FROM python:3.11-slim

WORKDIR /app

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY backend/ .

# Делаем скрипт исполняемым
RUN chmod +x /app/scripts/init.sh

EXPOSE 8000

CMD ["/app/scripts/init.sh"]