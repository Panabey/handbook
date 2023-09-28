FROM python:3.11-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/async_api /app

RUN pip install -r requirements.txt --no-cache-dir -U

WORKDIR /app/src

CMD ["uvicorn", "main:app", \
    "--workers", "4", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--log-level", "error", \
    "--ws", "none", \
    "--interface", "asgi3", \
    "--loop", "uvloop", \
    "--http", "httptools", \
    "--timeout-keep-alive", "30", \
    "--proxy-headers", \
    "--no-server-header" \
    ]
