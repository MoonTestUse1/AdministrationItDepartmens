FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ .

# Build the app
RUN npm run build

# Keep container running and serve the built files
CMD ["npm", "run", "preview"]
