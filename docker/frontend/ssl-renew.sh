#!/bin/sh

# Обновляем сертификат
certbot renew --quiet

# Перезагружаем nginx для применения обновленного сертификата
nginx -s reload 