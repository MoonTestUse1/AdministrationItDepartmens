FROM node:18

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Очищаем cache и node_modules
RUN npm cache clean --force
RUN rm -rf node_modules

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY frontend/ .

# Создаем .env файл
RUN echo "VITE_API_URL=/api" > .env

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
ENV HOST=0.0.0.0
CMD ["npm", "run", "dev"]