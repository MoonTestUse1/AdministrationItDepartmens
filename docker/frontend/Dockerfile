FROM node:18-alpine as build

WORKDIR /app

# Копируем только package.json и package-lock.json сначала
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем все остальные файлы фронтенда
COPY frontend/ .

# Собираем приложение
RUN npm run build

# Используем nginx для раздачи статики
FROM nginx:alpine

# Копируем собранные файлы из этапа сборки
COPY --from=build /app/dist /usr/share/nginx/html

# Создаем необходимые директории для nginx
RUN mkdir -p /var/cache/nginx \
             /var/cache/nginx/client_temp \
             /var/cache/nginx/proxy_temp \
             /var/cache/nginx/fastcgi_temp \
             /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
