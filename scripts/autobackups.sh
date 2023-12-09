#!/bin/bash

# Переменные
DB_CONTAINER_NAME="postgresql_handbook"
DB_USER="handbook_user"
DB_NAME="handbook"
BACKUP_DIR="/root/backups"
PASSWORD="!dropmecode" # change
MAX_BACKUPS=3

# Создание имени файла бэкапа с датой
TIMESTAMP=$(date +%Y_%m_%d_%H_%M_%S)
BACKUP_TEMP_FILE="$BACKUP_DIR/tmp/$DB_NAME-$TIMESTAMP-dump.sql.gz"
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
docker exec -t $DB_CONTAINER_NAME pg_dump -U $DB_USER -d $DB_NAME | gzip -7 > $BACKUP_TEMP_FILE

# Заархивировать бэкап с паролем
zip --password $PASSWORD "$BACKUP_FILE.zip" $BACKUP_TEMP_FILE -j

# Удаление папки
rm -rf "$BACKUP_DIR/tmp/"

# Удаление старых бэкапов
cd $BACKUP_DIR

# Удаление старых бэкапов (оставить ровно MAX_BACKUPS бэкапов)
while [ $(ls $BACKUP_DIR/*.zip | wc -l) -gt $MAX_BACKUPS ]; do
  OLD_BACKUP=$(ls -t $BACKUP_DIR/*.zip | tail -n 1)
  rm $OLD_BACKUP
done
