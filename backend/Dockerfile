# Use Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create script to run migrations and start app
RUN echo '#!/bin/sh\n\
echo "Waiting for database..."\n\
sleep 5\n\
echo "Running migrations..."\n\
alembic upgrade head\n\
echo "Starting application..."\n\
python run.py' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Run migrations and start application
CMD ["/app/start.sh"] 