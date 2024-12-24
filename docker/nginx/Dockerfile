FROM nginx:alpine

# Copy configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /var/cache/nginx \ -12,21 +12,11 @@ RUN mkdir -p /var/cache/nginx \
             /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp \
             /var/run \
    && chmod -R 755 /var/cache/nginx \
    && chmod -R 755 /etc/nginx \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /etc/nginx

EXPOSE 8000

CMD ["nginx", "-g", "daemon off;"]
