FROM node:22.14-alpine AS build

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

# Copiar o código fonte
COPY . .

RUN yarn build

FROM nginx:alpine AS production

COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
