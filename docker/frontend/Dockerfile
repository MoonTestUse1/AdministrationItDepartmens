FROM node:18-alpine as build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

# Создаем необходимые директории и назначаем права
RUN mkdir -p /var/cache/nginx \
             /var/cache/nginx/client_temp \
             /var/cache/nginx/proxy_temp \
             /var/cache/nginx/fastcgi_temp \
             /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp \
             /var/run \
    && chmod 777 /var/cache/nginx \
                 /var/cache/nginx/client_temp \
                 /var/cache/nginx/proxy_temp \
                 /var/cache/nginx/fastcgi_temp \
                 /var/cache/nginx/uwsgi_temp \
                 /var/cache/nginx/scgi_temp \
                 /var/run

# Удаляем директиву user из конфига nginx
RUN sed -i '/user/d' /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]