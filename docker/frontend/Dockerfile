# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY frontend/ ./

# Собираем приложение
RUN npm run build

# Production stage
FROM nginx:alpine

# Копируем собранные файлы
COPY --from=build /app/dist /usr/share/nginx/html/

# Удаляем дефолтную страницу nginx
RUN rm -rf /usr/share/nginx/html/50x.html

# Копируем конфигурацию nginx
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]