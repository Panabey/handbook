FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/admin /app

RUN pip install -r requirements.txt --no-cache-dir -U && python manage.py collectstatic --noinput

CMD ["granian", \
    "--workers", "1", \
    "--interface", "wsgi", \
    "--host", "0.0.0.0", \
    "--port", "8001", \
    "--log-level", "error", \
    "--no-ws", \
    "admin.wsgi:application" \
    ]
