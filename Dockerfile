# syntax=docker/dockerfile:1
FROM ubuntu:focal

RUN apt update
RUN apt upgrade
RUN apt -y install python3.10
RUN apt -y install python3-pip
RUN pip install --upgrade pip -y

RUN python3.10 -m pip install spacy
RUN python3.10 -m spacy download en_core_web_sm


RUN install unixodbc-dev
RUN pip install pyodbc

WORKDIR /var/www

COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
#ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
# RUN pip install --upgrade pip





EXPOSE 5000
COPY . .
CMD ["python", "main.py"]