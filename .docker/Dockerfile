FROM python:3.6-slim
WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y

COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 5000
