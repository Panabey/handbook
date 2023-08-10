FROM python:3.11-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY backend/async_api/requirements.txt .
RUN python -m pip install -r requirements.txt --no-cache-dir -U

WORKDIR /app
COPY backend/async_api/src /app

CMD ["uvicorn", "main:app", \
    "--workers", "2", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--timeout-keep-alive", "30", \
    "--proxy-headers", \
    "--no-server-header" \
    ]
