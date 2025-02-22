FROM python:3.10-alpine

WORKDIR /app
RUN apt install -y libpq-dev gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
