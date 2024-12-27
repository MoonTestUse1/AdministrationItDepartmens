FROM nginx:alpine

# Копируем конфигурацию nginx
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

# Копируем собранные файлы фронтенда
COPY frontend/dist /usr/share/nginx/html/

# Удаляем дефолтную страницу nginx
RUN rm -rf /usr/share/nginx/html/50x.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]