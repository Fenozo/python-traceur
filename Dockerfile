# syntax=docker/dockerfile:1
FROM quay.io/astronomer/ap-airflow:1.10.14-1-buster-onbuild


WORKDIR /var/www



USER root

RUN apt-get update \
  && apt-get -y install gcc gnupg2 \
  && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update \
  && ACCEPT_EULA=Y apt-get -y install msodbcsql17 \
  && ACCEPT_EULA=Y apt-get -y install mssql-tools

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
  && source ~/.bashrc

RUN apt-get -y install unixodbc-dev \
  && apt-get -y install python-pip \
  && pip install pyodbc



COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
#ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
# RUN pip install --upgrade pip





EXPOSE 5000
COPY . /var/www
CMD ["python", "main.py"]