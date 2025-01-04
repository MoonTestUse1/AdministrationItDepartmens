FROM node:18

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY frontend/package*.json ./

# Очищаем cache и node_modules
RUN npm cache clean --force
RUN rm -rf node_modules

# Устанавливаем основные зависимости
RUN npm install

# Устанавливаем tailwind и его плагины
RUN npm install -D tailwindcss postcss autoprefixer @tailwindcss/forms

# Устанавливаем дополнительные зависимости
RUN npm install axios
RUN npm rebuild rollup

# Копируем исходный код
COPY frontend/ .

# Генерируем tailwind конфигурацию
RUN npx tailwindcss init -p

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]