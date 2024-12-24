#!/bin/bash

# Остановить все контейнеры
docker compose down

# Создать временную директорию для webroot
mkdir -p ./docker/certbot/www

# Запустить nginx
docker compose up -d frontend

# Подождать, пока nginx запустится
echo "Waiting for nginx to start..."
sleep 5

# Получить тестовый сертификат
docker compose run --rm certbot

# Если тестовый сертификат получен успешно, получить боевой сертификат
if [ $? -eq 0 ]; then
    echo "Test certificate obtained successfully. Getting production certificate..."
    docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/html --email admin@itformhelp.ru --agree-tos --no-eff-email --force-renewal -d itformhelp.ru -d www.itformhelp.ru
fi

# Перезапустить все сервисы
docker compose down
docker compose up -d
