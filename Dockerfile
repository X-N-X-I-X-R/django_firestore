# Use a Python runtime as a parent image
FROM python:3.11.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Add and run as non-root user
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Run Gunicorn
CMD gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
