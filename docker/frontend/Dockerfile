# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Копируем только файлы для установки зависимостей
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем остальные файлы проекта
COPY frontend/ .

# Собираем приложение
RUN npm run build

# Production stage
FROM nginx:alpine

# Устанавливаем certbot и необходимые пакеты
RUN apk add --no-cache certbot certbot-nginx

# Копируем конфигурацию nginx
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Копируем скрипт инициализации SSL
COPY docker/frontend/init-ssl.sh /docker-entrypoint.d/init-ssl.sh
RUN chmod +x /docker-entrypoint.d/init-ssl.sh

# Копируем только собранные файлы из build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Создаем директории для Let's Encrypt
RUN mkdir -p /var/www/certbot /etc/letsencrypt

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]