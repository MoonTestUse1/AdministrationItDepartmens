FROM node:18

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install
RUN npm rebuild rollup

# Копируем исходный код
COPY frontend/ .

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]