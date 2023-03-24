from maga.DbManager import DbManager

class Repository :
    def __init__(self):
        self.db = DbManager()
        self.conn = self.db.get_instance()
        self.cursor = self.conn.cursor()

    def getList(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except:
            return None
    
    def getOnFromDb(self, sql):
        cursor =  self.cursor
        cursor.execute(sql)
        data = cursor.fetchone()
        return data
    
    def checked(self, sql):
        cursor =  self.cursor
        data = []
        try:
            cursor.execute(sql)
            data = cursor.fetchone()
        except Exception as e:
            print(e)

        return data

    def getChecked(self, sql):
        cursor =  self.cursor
        print(sql)
       
        try:
            cursor.execute(sql)
            data = cursor.fetchone()
        except Exception as e:
            print(e)

        dataExist = False
        statut = 0

        if data is not None:
            dataExist = True
            statut= data.statut

        return {
            'statut' : statut
           , 'exit'  : dataExist
        }

    def executeSql(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit() # permet de persister les données dans la base
            return True
        except:
            return False
        # self.conn.close()

