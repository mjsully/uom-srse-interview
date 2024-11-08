FROM python:3.13-alpine

LABEL org.opencontainers.image.source=https://github.com/mjsully/fuel-prices-api 

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY *.py .