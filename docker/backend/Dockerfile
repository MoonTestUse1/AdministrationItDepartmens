FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем только requirements.txt сначала
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY ./backend /app/

CMD ["python", "run.py"]
