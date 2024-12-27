FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create logs directory
RUN mkdir -p /app/logs

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create volume for logs
VOLUME ["/app/logs"]

# Expose the port the app runs on
EXPOSE 8000

CMD ["python", "run.py"]