import pyodbc

class DbManager:
    __instance = None

    def get_instance(self) :
        if DbManager.__instance is None :
            DbManager.__instance = self.connection()
        return DbManager.__instance

    def connection(self):
        SERVER_NAME = '192.168.123.141' #Your server name 
        # SERVER_NAME = '127.0.0.1'
        DATABASE_NAME = 'commerciale' 
        UID = 'sa' #Your login
        PWD = 'commerciale' #Your login password
        cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER_NAME+';DATABASE='+DATABASE_NAME+';UID='+UID+';PWD='+ PWD
        conn = pyodbc.connect(cstr)
        return conn