# Builder
FROM node:14-alpine AS builder

RUN mkdir /app
WORKDIR /app

ADD package.json /app/
ADD package-lock.json /app/

COPY . /app/

RUN npm install


# Deploy
FROM builder
COPY ./ /autismdrive
WORKDIR /autismdrive/frontend/
RUN npm install -g @angular/cli
RUN npm install
CMD ng serve --host 0.0.0.0
