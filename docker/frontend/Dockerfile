FROM node:18-alpine

WORKDIR /app

# Copy package files from frontend directory
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source code
COPY frontend/ .

# Build the app
CMD ["npm", "run", "build"]
