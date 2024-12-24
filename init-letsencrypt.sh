#!/bin/bash

# Остановить все контейнеры
docker compose down -v

# Создать необходимые директории
mkdir -p ./certbot/www
mkdir -p ./certbot/conf

# Запустить только nginx для первичной проверки
docker compose up -d frontend

# Подождать, пока nginx запустится
sleep 5

# Запустить certbot для получения сертификата
docker compose run --rm certbot

# Перезапустить все сервисы
docker compose down
docker compose up -d
