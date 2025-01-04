# Build stage
FROM node:18

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY frontend/ .

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
ENV HOST=0.0.0.0
CMD ["npm", "run", "dev"]

# Production stage
FROM nginx:alpine

# Копируем конфигурацию nginx и собранные файлы
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]