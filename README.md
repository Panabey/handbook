## Backend для справочника dropmecode.ru

### Первичный запуск проекта
1. `$ git clone https://github.com/Panabey/handbook.git`
2. `$ docker-compose up -d postgresql`
3. `$ docker-compose up -d --build async_api`
4. `$ docker exec -it <id_контейнера> /bin/bash`
5. `$ cd ..`
6. `$ alembic upgrade head` (Выйти из контейнера и на всякий повторно перезапустить)
7. `$ docker-compose build admin`
8. `$ docker volume create --name=shared-media` (Если потребуется)
9. `$ docker-compose up -d admin`
10. `$ docker exec -it <id_контейнера> /bin/bash`
11. `$ python manage.py makemigrations && python manage.py migrate`
12. `$ python manage.py createsuperuser` (Выйти из контейнера)
13. `$ docker-compose up -d` или `$ docker-compose up -d <имя_контейнера>`

### Запуск при обновлении
1. `$ git pull`
2. `$ docker-compose up -d --build async_api` (Обновить то, где были изменения)
3. Если потребуется, то провести миграции БД через **alembic** или **django ORM**

### FAQ

1. Что делать если произошла блокировка пользователя в admin панели?

Если доступ к учётной записи суперпользователя заблокирован, то перейдите в docker контейнер с панелью администрирования и введите одну из команд:

- `python manage.py axes_reset` - сбросит все блокировки и записи доступа.
- `python manage.py axes_reset_ip [ip ...]` - сбросит блокировки и записи для данных IP-адресов.
- `python manage.py axes_reset_username [username ...]` - сбросит блокировки и записи для данных имен пользователей.
- `python manage.py axes_reset_logs (age)` - сбросит (т. е. удалит) записи AccessLog старше заданного возраста (по умолчанию - 30 дней).

> Но если возможность к панели имеется, то просто удалите соответствующую запись в "Попытки доступа".

### Структура проекта

Back-end разделён на несколько частей:

Django 4.2+ - по пути `/backend/admin`

FastAPI 0.100+ по пути `/backend/async_api/src`
