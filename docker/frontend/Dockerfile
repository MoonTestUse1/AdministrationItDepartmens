# Этап сборки
FROM node:18-alpine as builder

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем исходный код
COPY . .

# Собираем приложение
RUN npm run build

# Этап production
FROM nginx:alpine

# Копируем собранные файлы из этапа сборки
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем конфигурацию nginx
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

# Указываем команду для запуска nginx
CMD ["nginx", "-g", "daemon off;"]
