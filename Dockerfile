FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . .

RUN ./install.sh

CMD "rocketload"