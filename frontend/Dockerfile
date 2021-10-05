FROM node:16.4.2-alpine

WORKDIR /frontend

COPY package*.json ./

RUN npm install -g @angular/cli @angular-devkit/build-angular && npm install

EXPOSE 4200

