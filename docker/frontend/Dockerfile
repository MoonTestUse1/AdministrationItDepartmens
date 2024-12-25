# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Debug: Show working directory
RUN pwd && ls -la

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ ./

# Debug: Show files before build
RUN echo "Files before build:" && ls -la

# Build the app
RUN npm run build

# Debug: Show build output
RUN echo "Build output:" && ls -la dist/

# Production stage
FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy static assets from builder stage
COPY --from=build /app/dist/ /usr/share/nginx/html/

# Copy nginx configuration
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

# Debug: Show copied files
RUN echo "Files in nginx html dir:" && ls -la /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]