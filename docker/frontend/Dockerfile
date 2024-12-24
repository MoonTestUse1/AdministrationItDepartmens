FROM node:18-alpine as build

WORKDIR /app

# Установите зависимости
COPY frontend/package*.json ./
RUN npm install

# Скопируйте исходный код и соберите приложение
COPY frontend/ .
RUN npm run build

FROM nginx:alpine

# Copy configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /var/cache/nginx \
             /var/cache/nginx/client_temp \
             /var/cache/nginx/proxy_temp \
             /var/cache/nginx/fastcgi_temp \
             /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp \
             /var/run \
    && chmod -R 755 /var/cache/nginx \
    && chmod -R 755 /etc/nginx \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /etc/nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]