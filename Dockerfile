# Production Dockerfile for UPI-Shield FastAPI REST Backend
# Includes OS-level Tesseract OCR dependencies for screenshot scanning

FROM python:3.11-slim

# Prevent Python from writing .pyc files & enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install OS-level Tesseract OCR engine and language data
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency specification and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY src/ ./src/
COPY api/ ./api/
COPY data/ ./data/
COPY app.py .

# Render dynamically passes $PORT env var (defaults to 8000 for local container runs)
ENV PORT=8000
EXPOSE 8000

# Command to run uvicorn server binding to 0.0.0.0:$PORT
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
