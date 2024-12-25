FROM node:18-alpine

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY frontend/ ./

# Собираем приложение
RUN npm run build

# Держим контейнер запущенным
CMD ["tail", "-f", "/dev/null"]