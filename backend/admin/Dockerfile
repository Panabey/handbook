FROM python:3.11-slim

EXPOSE 8001

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/admin /app

RUN pip install -r requirements.txt --no-cache-dir -U && python manage.py collectstatic

CMD ["uvicorn", "admin.asgi:application", \
    "--workers", "1", \
    "--host", "0.0.0.0", \
    "--port", "8001", \
    "--lifespan", "off", \
    "--ws", "none", \
    "--proxy-headers", \
    "--no-server-header" \
    ]
