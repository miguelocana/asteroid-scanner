FROM node:lts-alpine

WORKDIR /app

COPY package*.json ./

COPY . ./

RUN npm install

RUN chown -R node:node /app/node_modules
RUN chmod -R 777  /app/node_modules
RUN mkdir /app/node_modules/.vite
RUN chown -R node:node /app/node_modules/.vite

USER node

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]