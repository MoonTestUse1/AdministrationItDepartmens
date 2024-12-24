FROM nginx:alpine

# Copy nginx configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# Create required directories and set permissions
RUN mkdir -p /var/cache/nginx \
             /var/cache/nginx/client_temp \
             /var/cache/nginx/proxy_temp \
             /var/cache/nginx/fastcgi_temp \
             /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp \
             /var/run \
    && chown -R nginx:nginx /var/cache/nginx \
                           /var/cache/nginx/client_temp \
                           /var/cache/nginx/proxy_temp \
                           /var/cache/nginx/fastcgi_temp \
                           /var/cache/nginx/uwsgi_temp \
                           /var/cache/nginx/scgi_temp \
                           /var/run \
    && chmod 755 /var/cache/nginx \
                 /var/cache/nginx/client_temp \
                 /var/cache/nginx/proxy_temp \
                 /var/cache/nginx/fastcgi_temp \
                 /var/cache/nginx/uwsgi_temp \
                 /var/cache/nginx/scgi_temp \
                 /var/run

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]