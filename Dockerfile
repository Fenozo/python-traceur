# syntax=docker/dockerfile:1
FROM python:3.10-alpine

RUN pip install --upgrade pip
WORKDIR /var/www

RUN  apt-get update -y apt-get install -y python-pyodbc

#ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
# RUN pip install --upgrade pip



COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "main.py"]