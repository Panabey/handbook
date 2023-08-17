## Backend для справочника dropmecode.ru

### Запуск проекта
1. `$ git clone https://github.com/Panabey/handbook.git`
2. `$ docker-compose up -d postgresql`
3. `$  docker-compose build async_api`
4. `$ docker-compose up -d async_api`
5. `$ docker exec -it <id_контейнера> /bin/bash`
6. `$ cd ..`
7. `$ alembic upgrade head` (Выйти из контейнера и на всякий повторно перезапустить)
8. `$ docker-compose build admin`
9. `$ docker volume create --name=shared-media` (Если потребуется)
10. `$ docker-compose up -d admin`
11. `$ docker exec -it <id_контейнера> /bin/sh`
12. `$ python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic`
13. `$ python manage.py createsuperuser` (Выйти из контейнера)
14. `$ docker-compose up -d`

### Структура проекта

Back-end разделён на несколько частей:

Django 4.2+ - по пути `/backend/admin`

FastAPI 0.100+ по пути `/backend/async_api/src`
