FROM python:3.11-slim

EXPOSE 8001

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/admin /app

RUN pip install httptools -r requirements.txt --no-cache-dir -U

CMD ["uvicorn", "admin.wsgi:application", \
    "--workers", "1", \
    "--host", "0.0.0.0", \
    "--port", "8001", \
    "--lifespan", "off", \
    "--interface", "wsgi", \
    "--ws", "none", \
    "--http", "httptools", \
    "--proxy-headers", \
    "--no-server-header" \
    ]
