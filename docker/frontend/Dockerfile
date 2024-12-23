FROM node:18-alpine as builder

WORKDIR /app

# Копируем файлы package.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем исходники
COPY frontend/ ./

# Собираем приложение
RUN npm run build

# Финальный этап
FROM scratch
COPY --from=builder /app/dist /dist
