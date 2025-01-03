FROM python:3.11-slim

WORKDIR /app

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y netcat-traditional dos2unix && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY backend/ .

# Делаем скрипт исполняемым и устанавливаем правильные права
RUN chmod +x /app/scripts/init.sh && \
    chown -R root:root /app/scripts/init.sh && \
    dos2unix /app/scripts/init.sh

EXPOSE 8000

CMD ["/bin/bash", "/app/scripts/init.sh"]