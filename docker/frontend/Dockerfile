FROM node:20-alpine as build

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

COPY frontend .

RUN npm run build

FROM nginx:alpine

# Установка certbot
RUN apk add --no-cache certbot certbot-nginx

COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Создаем директории для сертификатов и certbot
RUN mkdir -p /etc/letsencrypt
RUN mkdir -p /var/www/certbot

# Копируем скрипты
COPY docker/frontend/ssl-renew.sh /etc/periodic/daily/ssl-renew
COPY docker/frontend/init-ssl.sh /docker-entrypoint.d/init-ssl.sh
RUN chmod +x /etc/periodic/daily/ssl-renew
RUN chmod +x /docker-entrypoint.d/init-ssl.sh

EXPOSE 80 443

# Запускаем crond и nginx
CMD ["sh", "-c", "crond && /docker-entrypoint.d/init-ssl.sh"]