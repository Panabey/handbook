#!/bin/bash

# Переменные
DB_CONTAINER_NAME="postgresql"
DB_USER="user" # change
DB_NAME="handbook"
BACKUP_DIR="/path" # change
PASSWORD="password" # change
MAX_BACKUPS=2

# Создание имени файла бэкапа с датой
TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_TEMP_FILE="$BACKUP_DIR/tmp/$DB_NAME-$TIMESTAMP-dump.gz"
BACKUP_FILE="$BACKUP_DIR/$DB_NAME-$TIMESTAMP"

# Создать директорию для бэкапов, если она не существует
mkdir -p "$BACKUP_DIR/tmp/"

CONTAINER_ID=$(docker ps -q -f name=$DB_CONTAINER_NAME)

# Проверить, найден ли контейнер
if [ -z "$CONTAINER_ID" ]; then
  echo "Контейнер с именем $DB_CONTAINER_NAME не найден."
  exit 1
fi

# Выполнить резервное копирование внутри контейнера
docker exec -t $CONTAINER_ID pg_dump -U $DB_USER $DB_NAME --no-indexes | gzip > $BACKUP_TEMP_FILE

# Заархивировать бэкап с паролем
zip --password $PASSWORD $BACKUP_FILE.zip $BACKUP_TEMP_FILE

# Удаление папки
rm -rf "$BACKUP_DIR/tmp/"

# Удаление старых бэкапов
cd $BACKUP_DIR

# Удаление старых бэкапов (оставить ровно MAX_BACKUPS бэкапов)
while [ $(ls $BACKUP_DIR/*.zip | wc -l) -gt $MAX_BACKUPS ]; do
  OLD_BACKUP=$(ls -t $BACKUP_DIR/*.zip | tail -n 1)
  rm $OLD_BACKUP
done
