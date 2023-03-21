FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

USER root

WORKDIR /var/www

RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static


# RUN /usr/bin/curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
#     /usr/bin/curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssqlrelease.list


# RUN apt-get update \
#   && ACCEPT_EULA=Y apt-get -y install msodbcsql17 \
#   && ACCEPT_EULA=Y apt-get -y install mssql-tools

# RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
#   && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
#   && source ~/.bashrc

# RUN apt-get -y install unixodbc-dev \
#   && apt-get -y install python-pip 

RUN apt-get update && apt-get install curl -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN exit
RUN apt-get update
RUN echo msodbcsql18 msodbcsql/ACCEPT_EULA boolean true | debconf-set-selections
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
    && /bin/bash -c "source ~/.bashrc"

# upgrade pip version
RUN pip install --upgrade pip


COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

EXPOSE 80

COPY . /var/www
CMD ["python", "main.py"]