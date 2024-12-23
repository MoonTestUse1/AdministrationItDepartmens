FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем только requirements.txt сначала
# Копируем остальные файлы
COPY ./backend /app/

CMD ["python", "run.py"]
