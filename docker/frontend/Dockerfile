FROM node:18-alpine

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY frontend/ .

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
CMD ["npm", "run", "dev", "--", "--host"]