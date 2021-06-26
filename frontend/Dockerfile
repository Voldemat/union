FROM node:14

ENV NODE_ENV=development


WORKDIR /frontend

RUN apt-get update && yes | apt-get install inotify-tools

ADD . /frontend

RUN npm install