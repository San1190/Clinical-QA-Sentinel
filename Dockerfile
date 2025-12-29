# ============================================================================
# Clinical-QA-Sentinel - Multi-Stage Dockerfile
# ============================================================================
# Purpose: Containerize the QA automation framework for portable execution
# Usage: docker build -t clinical-qa-sentinel .
#        docker run --rm clinical-qa-sentinel

# Base image - Python slim for smaller image size
FROM python:3.11-slim

# ============================================================================
# Metadata
# ============================================================================
LABEL maintainer="Clinical-QA-Sentinel Team"
LABEL description="Enterprise QA Automation Framework for Healthcare Systems"
LABEL version="1.0.0"

# ============================================================================
# Environment Variables
# ============================================================================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    ENVIRONMENT=demo \
    HEADLESS_MODE=true

# ============================================================================
# Install System Dependencies
# ============================================================================
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ============================================================================
# Install Google Chrome
# ============================================================================
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ============================================================================
# Set Working Directory
# ============================================================================
WORKDIR /app

# ============================================================================
# Copy Requirements and Install Python Dependencies
# ============================================================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================================================
# Copy Application Code
# ============================================================================
COPY . .

# ============================================================================
# Create Output Directories
# ============================================================================
RUN mkdir -p reports screenshots logs data

# ============================================================================
# Healthcheck (optional)
# ============================================================================
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# ============================================================================
# Default Command - Run Tests
# ============================================================================
# Default: Run pytest with HTML report
CMD ["pytest", "tests/", "--html=reports/test_report.html", "--self-contained-html", "-v"]

# Alternative commands (override when running container):
# Run patient data generator:
#   docker run --rm -v $(pwd)/data:/app/data clinical-qa-sentinel python src/patient_data_generator.py
#
# Run specific test:
#   docker run --rm clinical-qa-sentinel pytest tests/test_authentication.py -v
#
# Interactive shell:
#   docker run --rm -it clinical-qa-sentinel /bin/bash
