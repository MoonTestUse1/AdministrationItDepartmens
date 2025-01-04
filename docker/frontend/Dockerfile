FROM node:18

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Очищаем cache и node_modules
RUN npm cache clean --force && \
    rm -rf node_modules package-lock.json

# Устанавливаем все зависимости включая devDependencies
RUN npm install && \
    npm install -D @tailwindcss/forms && \
    npm cache clean --force

# Копируем конфигурационные файлы
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./
COPY frontend/vite.config.ts ./
COPY frontend/tsconfig.json ./
COPY frontend/tsconfig.node.json ./

# Копируем остальной исходный код
COPY frontend/ .

# Открываем порт для Vite
EXPOSE 5173

# Запускаем Vite сервер
ENV HOST=0.0.0.0
ENV NODE_ENV=development
CMD ["npm", "run", "dev"]