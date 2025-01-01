FROM node:18-alpine

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

# В dev режиме не копируем исходники, они будут монтироваться через volume
CMD ["npm", "run", "dev"]