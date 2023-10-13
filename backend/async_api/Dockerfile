FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/async_api /app

RUN pip install -r requirements.txt --no-cache-dir -U

WORKDIR /app/src

CMD ["granian", \
    "--workers", "4", \
    "--interface", "asgi", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--log-level", "error", \
    "--no-ws", \
    "--loop", "uvloop", \
    "main:app" \
    ]
