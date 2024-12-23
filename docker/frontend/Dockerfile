FROM node:18-alpine as build

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY . .

# Собираем приложение
RUN npm run build

# Копируем собранные файлы в volume
VOLUME ["/dist"]
CMD ["cp", "-r", "/app/dist/.", "/dist/"]