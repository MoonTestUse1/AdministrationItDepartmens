FROM node:18

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY frontend/package*.json ./

# Очищаем cache и node_modules
RUN npm cache clean --force
RUN rm -rf node_modules

# Устанавливаем зависимости через npm ci для точного соответствия package-lock.json
RUN npm ci

# Копируем исходный код
COPY frontend/ .

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]