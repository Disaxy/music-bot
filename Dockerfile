FROM python:3.7-slim

RUN mkdir /application

WORKDIR /application

COPY /app config.ini main.py requirements.txt ./

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -Ur requirements.txt

ENTRYPOINT [ "python", "main.py" ]