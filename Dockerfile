FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (ffmpeg, curl, etc)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/cache /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Default command
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
