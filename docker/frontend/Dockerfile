FROM node:18-alpine as build

WORKDIR /app

# Установите зависимости
COPY frontend/package*.json ./
RUN npm install

# Скопируйте исходный код и соберите приложение
COPY frontend/ .
RUN npm run build

FROM nginx:alpine

# Скопируйте собранные файлы в Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Скопируйте конфигурацию Nginx
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]