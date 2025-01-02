#!/bin/sh

# Проверяем наличие сертификата
if [ ! -f "/etc/letsencrypt/live/itformhelp.ru/fullchain.pem" ]; then
    echo "Сертификат не найден. Получаем новый..."
    
    # Останавливаем nginx для освобождения 80 порта
    nginx -s stop || true
    
    # Ждем освобождения порта
    sleep 5
    
    # Получаем сертификат
    certbot certonly --standalone \
        --email crocoman7887@gmail.com \
        --agree-tos \
        --no-eff-email \
        --non-interactive \
        -d itformhelp.ru
        
    # Проверяем успешность получения сертификата
    if [ ! -f "/etc/letsencrypt/live/itformhelp.ru/fullchain.pem" ]; then
        echo "Ошибка получения сертификата"
        exit 1
    fi
    
    echo "Сертификат успешно получен"
else
    echo "Сертификат уже существует"
fi

# Запускаем nginx с новой конфигурацией
echo "Запускаем nginx..."
nginx -g "daemon off;" 