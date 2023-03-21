FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

WORKDIR /var/www

RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

EXPOSE 6000

COPY . /var/www
CMD ["python", "main.py"]