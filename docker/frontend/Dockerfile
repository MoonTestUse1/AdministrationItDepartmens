FROM node:18

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Устанавливаем Tailwind и его зависимости
RUN npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

# Инициализируем Tailwind
RUN npx tailwindcss init -p

# Копируем исходный код
COPY frontend/ .

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
ENV HOST=0.0.0.0
CMD ["npm", "run", "dev", "--", "--host"]