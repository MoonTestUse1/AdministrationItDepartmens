# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Копируем только файлы для установки зависимостей
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install --production

# Копируем остальные файлы проекта
COPY frontend/ .

# Собираем приложение
RUN npm run build

# Production stage
FROM nginx:alpine

# Устанавливаем certbot
RUN apk add --no-cache certbot certbot-nginx

# Копируем конфигурацию nginx и собранные файлы
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем скрипт SSL и создаем директории
COPY docker/frontend/init-ssl.sh /docker-entrypoint.d/init-ssl.sh
RUN chmod +x /docker-entrypoint.d/init-ssl.sh && \
    mkdir -p /var/www/certbot /etc/letsencrypt

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]