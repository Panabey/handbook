FROM python:3.11-alpine

EXPOSE 8001

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY backend/admin/requirements.txt .
RUN python -m pip install -r requirements.txt --no-cache-dir -U

WORKDIR /app
COPY backend/admin /app

RUN python manage.py makemigrations

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
