FROM python:3.7-alpine

RUN mkdir /home/application

WORKDIR /home/application

RUN apk add --update gcc libssl-dev && rm -rf /var/cache/apk/* && cd /home/application

COPY /app config.ini main.py requirements.txt ./

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt