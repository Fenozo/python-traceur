# resolve bug from  DRIVER={ODBC Driver 17 for SQL Server};

[url]: https://stackoverflow.com/questions/44527452/cant-open-lib-odbc-driver-13-for-sql-server-sym-linking-issue

I simply built image top of python:3.7-alpine

FROM python:3.7-alpine

COPY . /app/.
WORKDIR /app

# Install curl
RUN apk add --no-cache curl
RUN apk update && apk add curl

# Install the Microsoft ODBC driver Linux.Follow the mssql documentation: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.8.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.8.1.1-1_amd64.apk

# Install the package(s)
RUN apk add --allow-untrusted msodbcsql17_17.8.1.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.8.1.1-1_amd64.apk

# Install other libs
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apk add python3 python3-dev g++ unixodbc-dev
RUN python3 -m ensurepip
RUN pip3 install --user pyodbc

# Run script
ENTRYPOINT [ "python", "-u", "run.py"]

-------------------------------------------------------------------------------------------------------------------
# notes for php checkout version
sudo update-alternatives --config php

# Création d'une pagination sur sql server 2008
-------------------------------------------------------------------------------
DECLARE @PageNo  INT=10
DECLARE @PageSize INT=10

select  id_traceur, numblf , Nom_personnel, MatSaisie, Prefixe, Rs, CP, District, Province
from(

	select id_traceur, numblf , Nom_personnel, MatSaisie, Prefixe, Rs, CP, District, Province,
	ROW_NUMBER() over (order by numblf) as RowNum
	from [aya_magasin_tache_table]
)T 

WHERE T.RowNum BETWEEN ((@PageNo-1) * @PageSize)+1 AND (@PageNo * @PageSize) order by id_traceur ASC

-------------------------------------------------------------------------------
select COUNT(*)/10 + 1
from [aya_magasin_tache_table]
-------------------------------------------------------------------------------
	

