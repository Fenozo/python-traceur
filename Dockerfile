# syntax=docker/dockerfile:1
FROM ubuntu:20.04

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

RUN apt-get update && apt-get install python3.10
RUN pip install --upgrade pip

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