FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

USER root

WORKDIR /var/www

RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

# install pyodbc mais avant on install dans apline avec apk commande le g++ unixodbc-dev compilateur
RUN apk add python3 python3-dev g++ unixodbc-dev 
RUN python3 -m ensurepip
RUN pip3 install --user pyodbc

# upgrade pip version
RUN pip install --upgrade pip

RUN python -m pip install wheel


COPY ./requirements.txt /var/www/requirements.txt
RUN python -m pip wheel -r /var/www/requirements.txt

EXPOSE 80

COPY . /var/www
CMD ["python", "main.py"]