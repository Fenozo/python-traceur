FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

WORKDIR /var/www

RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static


RUN /usr/bin/curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    /usr/bin/curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssqlrelease.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install msodbcsql=13.1.9.2-1 mssql-tools=14.0.6.0-1 unixodbc-dev -y 

# upgrade pip version
RUN pip install --upgrade pip

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

EXPOSE 80

COPY . /var/www
CMD ["python", "main.py"]