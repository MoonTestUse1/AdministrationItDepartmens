FROM nginx:alpine

# Установка certbot и зависимостей
RUN apk add --no-cache certbot certbot-nginx openssl

# Копирование скриптов и конфигурации
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./docker/nginx/entrypoint.sh /entrypoint.sh

# Создание директорий для certbot
RUN mkdir -p /var/www/certbot && \
    mkdir -p /etc/letsencrypt && \
    chmod +x /entrypoint.sh

# Установка правильных прав для nginx
RUN chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    chown -R nginx:nginx /var/www/certbot && \
    chmod -R 755 /var/www/certbot

ENTRYPOINT ["/entrypoint.sh"]