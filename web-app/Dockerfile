# Step 1: Build
FROM node:16 AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Step 2: Serve
FROM nginx:stable-alpine
# Copy the build output to NGINX html folder
COPY --from=build-stage /app/dist /usr/share/nginx/html
# Copy custom nginx config (SPA routing + /api proxy to backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
