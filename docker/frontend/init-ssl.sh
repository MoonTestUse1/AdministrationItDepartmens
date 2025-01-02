#!/bin/sh

# Остановка nginx
nginx -s stop || true

# Получение сертификата
certbot certonly --standalone \
  --email crocoman7887@gmail.com \
  --agree-tos \
  --no-eff-email \
  --staging \
  -d itformhelp.ru

# После успешного получения сертификата в staging, получаем боевой сертификат
certbot certonly --standalone \
  --email crocoman7887@gmail.com \
  --agree-tos \
  --no-eff-email \
  --force-renewal \
  -d itformhelp.ru

# Запуск nginx
nginx -g "daemon off;" 