# Use Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
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
while ! pg_isready -h db -p 5432 -U postgres; do\n\
  sleep 1\n\
done\n\
echo "Database is ready!"\n\
echo "Running migrations..."\n\
cd /app && alembic upgrade head\n\
echo "Starting application..."\n\
python run.py' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Run migrations and start application
CMD ["/app/start.sh"] 