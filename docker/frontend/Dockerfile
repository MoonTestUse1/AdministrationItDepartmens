# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем все зависимости
RUN npm install

# Копируем исходный код
COPY frontend/ .

# Собираем приложение
RUN npm run build

# Production stage
FROM nginx:alpine

# Копируем конфигурацию nginx и собранные файлы
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

# Создаем директорию для pid файла
RUN mkdir -p /var/run/nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]