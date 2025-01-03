#!/bin/sh

# Домены для SSL-сертификата
domains="itformhelp.ru www.itformhelp.ru"
email="admin@itformhelp.ru"

# Функция для получения сертификата
get_certificate() {
    echo "Requesting Let's Encrypt certificate for $domains ..."
    
    # Создаем временный конфиг nginx для валидации certbot
    cat > /etc/nginx/conf.d/temp.conf << EOF
server {
    listen 80;
    server_name $domains;
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://\$host\$request_uri;
    }
}
EOF

    # Перезапускаем nginx с временным конфигом
    nginx -t && nginx -s reload

    # Запрашиваем сертификат
    certbot certonly --webroot \
        --webroot-path=/var/www/certbot \
        --email $email \
        --agree-tos \
        --no-eff-email \
        --force-renewal \
        -d $(echo $domains | sed 's/ / -d /g')

    # Удаляем временный конфиг
    rm /etc/nginx/conf.d/temp.conf
}

# Проверяем наличие сертификата
if [ ! -d "/etc/letsencrypt/live/itformhelp.ru" ]; then
    get_certificate
fi

# Запускаем фоновый процесс для автоматического обновления сертификатов
while :; do
    certbot renew --deploy-hook "nginx -s reload"
    sleep 12h
done &

# Запускаем nginx
nginx -g "daemon off;" 