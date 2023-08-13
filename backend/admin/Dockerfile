FROM python:3.11-alpine

EXPOSE 8001

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/admin/requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir -U

COPY backend/admin /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
