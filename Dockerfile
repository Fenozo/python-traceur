FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

WORKDIR /var/www

RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static


RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install msodbcsql mssql-tools unixodbc-dev -y 

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
# upgrade pip version
RUN pip install --upgrade pip

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

EXPOSE 80

COPY . /var/www
CMD ["python", "main.py"]