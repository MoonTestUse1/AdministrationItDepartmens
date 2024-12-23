FROM node:18-alpine as build

# Установим рабочую директорию
WORKDIR /app

# Копируем файлы package.json и package-lock.json из директории frontend
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код из директории frontend
COPY frontend/ .

# Собираем приложение
RUN npm run build

# Используем nginx для раздачи статики
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

# Используем пользователя nginx
USER nginx
