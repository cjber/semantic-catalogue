# Use an official Node.js image to build the React app
FROM node:16-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the React application
RUN npm run build

# Use a lightweight image to serve the content
FROM node:16-alpine AS serve

# Install the 'serve' package to serve static files
RUN npm install -g serve

# Copy the built files from the previous stage
COPY --from=build /app/build /app/build

# Set the working directory to the build directory
WORKDIR /app

# Expose the port your application will run on
EXPOSE 8001

# Command to serve the application
CMD ["serve", "-s", "build", "-l", "8001"]
