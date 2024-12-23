# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies using npm install instead of npm ci
COPY package*.json ./
RUN npm install

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

# Add health check endpoint
RUN echo "health_check() { echo 'OK'; } && health_check > /usr/share/nginx/html/health" > /docker-entrypoint.d/40-health-check.sh

# Use non-root user
USER nginx
