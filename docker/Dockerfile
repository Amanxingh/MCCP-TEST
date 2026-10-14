
# Use Python 3.12 slim image
FROM python:3.12-slim

# Prevent Python from writing bytecode files
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy requirements and vendor packages from the project root
COPY requirements-dev.txt .
COPY vendor/ ./vendor/

# Install pytest offline using locally available packages
RUN python -m pip install --no-index --find-links=vendor pytest

# Copy application source, tests, and environment verification script
COPY src/ ./src/
COPY tests/ ./tests/
COPY verify_env.py .

# Run the test suite by default
CMD ["python", "-m", "pytest", "-v"]
