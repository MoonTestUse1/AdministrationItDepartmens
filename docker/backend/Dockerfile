FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем остальные файлы
COPY ./backend /app/

CMD ["python", "run.py"]
