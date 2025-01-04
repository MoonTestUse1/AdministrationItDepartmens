FROM node:18

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY frontend/package*.json ./

# Очищаем cache и node_modules
RUN npm cache clean --force
RUN rm -rf node_modules

# Устанавливаем зависимости и обновляем package-lock.json
RUN npm install

# Копируем исходный код
COPY frontend/ .

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
ENV HOST=0.0.0.0
CMD ["npm", "run", "dev", "--", "--host"]