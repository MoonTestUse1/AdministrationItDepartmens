FROM node:18-alpine

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY frontend/ ./

# Открываем порт для разработки
EXPOSE 5173

# Запускаем в режиме разработки
CMD ["npm", "run", "dev", "--", "--host"]