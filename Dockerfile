FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

USER root

WORKDIR /var/www

RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

# Install curl
RUN apk add --no-cache curl
RUN apk update && apk add curl

# Install the Microsoft ODBC driver Linux.Follow the mssql documentation: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.8.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.8.1.1-1_amd64.apk


# Install the package(s)
RUN apk add --allow-untrusted msodbcsql17_17.8.1.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.8.1.1-1_amd64.apk

# install pyodbc mais avant on install dans apline avec apk commande le g++ unixodbc-dev compilateur
RUN apk add python3 python3-dev g++ unixodbc-dev 
RUN python3 -m ensurepip
RUN pip3 install --user pyodbc

# upgrade pip version
RUN pip install --upgrade pip

RUN python -m pip install wheel

# if we don't have pip in your PATH environment variable
RUN python -m pip install Flask-Cors
# or python 3 (could also be pip3.10 depending on your version)
# RUN python3 -m pip install Flask-Cors

# if we don't have pip in your PATH environment variable
RUN python -m pip install flask_socketio

# if we don't have pip in your PATH environment variable
RUN python -m pip install Flask-Session

RUN python -m pip install simple-websocket



COPY ./requirements.txt /var/www/requirements.txt
RUN python -m pip wheel -r /var/www/requirements.txt

EXPOSE 9000

COPY . /var/www
CMD ["python", "main.py"]