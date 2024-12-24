FROM node:18-alpine as build

WORKDIR /app

# Copy package files from frontend directory
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source code
COPY frontend/ .

# Build the app
RUN npm run build

FROM nginx:alpine

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Create nginx config directory
RUN mkdir -p /etc/nginx/conf.d

# Copy nginx configuration
COPY docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

# Create required directories and set permissions

# Remove user directive from nginx config
RUN sed -i '/user/d' /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]