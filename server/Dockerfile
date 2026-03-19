FROM node:22-alpine

WORKDIR /app

# Install dependencies first for better layer caching
COPY server/package*.json ./
RUN npm install

# Copy TypeScript sources and build
COPY server/ ./
RUN npm run build

ENV NODE_ENV=production
ENV PORT=80

EXPOSE 80

CMD ["npm", "run", "start"]
