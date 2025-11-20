# Dockerfile (recommended)
FROM python:3.10-slim

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libgobject-2.0-0 \
    shared-mime-info \
    fonts-liberation \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "LG.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
