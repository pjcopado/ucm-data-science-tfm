#  Construcción
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

# Producción
FROM node:20-alpine AS runner

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --only=production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.ts ./next.config.ts
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]
