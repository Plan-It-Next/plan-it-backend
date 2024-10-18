# Use a minimal base image with Node.js 14
FROM node:14-alpine

# Set working directory in container
WORKDIR /app

# Install git to clone the repository
RUN apk add --no-cache git

# Clone the repository from GitHub
RUN git clone https://github.com/apache/age-viewer.git .

# Install node modules
RUN npm install

# Expose the port the app runs on
EXPOSE 3000

# Install pm2 globally
RUN npm install pm2

RUN npm run setup

# Set default command to run the application
CMD ["npm", "run", "start"]