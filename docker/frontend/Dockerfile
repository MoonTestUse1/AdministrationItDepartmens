FROM node:18

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Очищаем cache и node_modules
RUN npm cache clean --force
RUN rm -rf node_modules package-lock.json

# Устанавливаем зависимости
RUN npm install
RUN npm install axios@1.6.2

# Копируем исходный код
COPY frontend/ .

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
ENV HOST=0.0.0.0
CMD ["npm", "run", "dev"]