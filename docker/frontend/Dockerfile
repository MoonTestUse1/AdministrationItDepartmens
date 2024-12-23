# docker/frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Copy built files to nginx html directory
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
