FROM python:3.7-slim as base

FROM base as init

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

EXPOSE 5000

FROM base as build

RUN mkdir /application

WORKDIR /application

COPY /app config.ini requirements.txt ./

RUN pip install -Ur requirements.txt

ENTRYPOINT [ "python", "bot.py" ]