# Multi-stage Dockerfile for LogSentinel
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements*.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy source code
COPY . .

# Create directories for logs and rules
RUN mkdir -p /app/logs /app/rules /app/config

# Set up volume mounts
VOLUME ["/app/logs", "/app/rules", "/app/config"]

# Default command for development
CMD ["python", "-m", "pytest", "--cov=src/log_security", "--cov-report=term-missing", "--cov-report=html"]

# Production stage
FROM base as production

# Copy source code
COPY src/ ./src/
COPY config/ ./config/

# Create directories for logs and rules
RUN mkdir -p /app/logs /app/rules

# Set up volume mounts
VOLUME ["/app/logs", "/app/rules"]

# Default command for production
CMD ["python", "-m", "logsentinel.main"]
