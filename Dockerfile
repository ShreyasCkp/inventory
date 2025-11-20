FROM python:3.10-slim

# Install system deps for WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libglib2.0-0 \
    libgirepository1.0-dev libffi-dev shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "LG.wsgi:application", "--bind", "0.0.0.0:8000"]
