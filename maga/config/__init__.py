# from maga.config.BlfRepository import BlfRepository

from datetime import datetime
import sys
import pyodbc



class Configuration :
    def __init__(self) -> None:

        self.config = {
            'ipServer' : '0.0.0.0'
            ,'ipServerSocket' : '192.168.123.254'
            ,'port' :'9000'
        }

    def getIpServerSocket(self):
        return self.config['ipServerSocket']
    
    def getIpServer(self):
        return self.config['ipServer']
    
    def getPort(self):
        return self.config['port']
    
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
    


class Repository :
    def __init__(self):
        self.db = DbManager()
        self.conn = self.db.get_instance()
        self.cursor = self.conn.cursor()

    def getList(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
    
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


class BlfRepository(Repository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name='[Commerciale].[dbo].[aya_magasin_tache_table]' 
        self.BeforeDR  = '0'
        self.DR  = '1'
        self.FR  = '2'
        self.DEm = '3'
        self.FEm = '4' # Fin Emballage
        self.PE  = '5' # Préparation Expédition
        self.Exp = '6' # Expédition
        self.Text = {
             int(self.DR) : 'Début ramassage'
            ,int(self.FR) : 'Fin ramassage'
            ,int(self.DEm) : 'Début emballage'
            ,int(self.FEm) : 'Fin emballage'
            ,int(self.PE) : 'Préparation Expédition'
            ,int(self.Exp) : 'Expédition'
        }


    def getDateUpdate(self):
            now = datetime.now()
            self.datetimeformat = "%Y-%m-%d %H:%M.%S"
            self.measurementDateTime = now.strftime(self.datetimeformat)


    def getDataList(self, userId='', table_name='[Commerciale].[dbo].[aya_magasin_tache_table]'):
        
        sql = f"""--begin-sql 
            select NumBlf, Statut from {table_name}
            where 
            ([rs_ram] = {userId} or [rs_em] = {userId})
            and Statut > 0
            --end-sql"""

        return self.getList(sql=sql)
        
    def getListByUser(self, ID='', status=''):
        userId = ID
        sql = f""" --begin-sql
                select 
                id_traceur
                ,numblf
                ,statut
                from {self.table_name} 
                where 
                ([rs_ram] = {userId} 
                or [re_ram] = {userId}
                or [rs_em] = {userId}
                or [re_em] = {userId}
                or [resp_prepa_exp] = {userId}
                or [resp_exp] = {userId}
                )
                --and statut = {status}
                --end-sql
                """
        data = self.getList(sql)
        
        items = []
        for item in data:
            items.append({
                'id_traceur': item.id_traceur
                ,'numblf' : item.numblf
                ,'statut' : self.Text[item.statut]
                ,'statusNumber' : item.statut
            })

        return {
            'sql' : sql
            ,'data' : items
        }
    def debut_ramassage(self, numblf='', userId=''):
        self.getDateUpdate()
        check = self.check_avant_debut_ramassage(nblf=numblf, table_name=self.table_name)

        # print(check)
        # sys.exit()
        if  check['exit'] ==  False:
            print('IMPOSSIBLE DE PASSE ICI !')
            return False
        elif check['exit'] == True:
            sql = f""" --begin-sql
                update
                {self.table_name}

                set rs_ram = {userId} -- 
                , [Statut] = CONVERT(int, {self.DR})
                , [sd_ram] = CONVERT(datetime, '{self.measurementDateTime}', 21)
                , [st_ram] = CONVERT(datetime, '{self.measurementDateTime}', 21)
                    
                where numblf='{numblf}'
                --end-sql
                """
            #print(sql)
            return self.executeSql(sql=sql)

    def fin_ramassage(self,numblf='', userId=''):
        self.getDateUpdate()
        check = self.check_avant_fin_ramassage(nblf=numblf, table_name=self.table_name)
        if  check['exit'] ==  False:
            print('IMPOSSIBLE DE PASSE ICI !')
            return False
        elif check['exit'] == True:
            sql = f""" --begin-sql
                update
                {self.table_name}

                set re_ram = {userId} -- 
                , [statut] = CONVERT(int, {self.FR})
                , [se_ram] = CONVERT(datetime, '{self.measurementDateTime}', 21)-- seconde end ramassage
                , [ed_ram] = CONVERT(datetime, '{self.measurementDateTime}', 21)-- date fin ramassage
                    
                where numblf='{numblf}'
                --end-sql
                """
            return self.executeSql(sql=sql)

    def debut_emballage(self,numblf='', userId=''):
        self.getDateUpdate()
        check = self.check_avant_debut_emballage(nblf=numblf, table_name=self.table_name)
        if  check['exit'] ==  False:
            
            print('IMPOSSIBLE DE PASSE ICI !')
            return False
        elif check['exit'] == True:
            sql = f""" --begin-sql
                update
                {self.table_name}

                set [rs_em] = {userId} -- RespEmballage 
                , [statut] = CONVERT(int, {self.DEm})
                , [sd_em] = CONVERT(datetime, '{self.measurementDateTime}', 21) -- START DATE EMBALLAGE
                , [st_em] = CONVERT(datetime, '{self.measurementDateTime}', 21) -- START TIME EMBALLAGE
                    
                where numblf='{numblf}'
                --end-sql
                """
            print(sql)
            return self.executeSql(sql=sql)

    def fin_emballage(self,numblf='', userId=''):
        self.getDateUpdate()
        check = self.check_avant_fin_emballage(nblf=numblf, table_name=self.table_name)
        if  check['exit'] ==  False:
            print('IMPOSSIBLE DE PASSE ICI !')
            return False
        elif check['exit'] == True:
            sql = f""" --begin-sql
            update
                    {self.table_name}

                    set [re_em]  = {userId} -- RESPONSABLE END RAMASSAGE 
                    , [statut] = CONVERT(int, {self.FEm})
                    , [et_em] = CONVERT(datetime, '{self.measurementDateTime}', 21) -- END TIME EMBALLAGE
                    , [ed_em] = CONVERT(datetime, '{self.measurementDateTime}', 21) -- END DATE EMBALLAGE
                where numblf='{numblf}'
                    --end-sql
                """
            return self.executeSql(sql=sql)
    def prepa_expedition(self, numblf='', userId=''):
        self.getDateUpdate()
        check = self.check_avant_preparation_expedition(nblf=numblf, table_name=self.table_name)
        if  check['exit'] ==  False:
            print('IMPOSSIBLE DE PASSE ICI !')
            return False
        elif check['exit'] == True:
            sql = f""" --begin-sql
            update
                    {self.table_name}

                    set [resp_prepa_exp]  = {userId} -- responsable start prépa expédition 
                    , [statut] = CONVERT(int, {self.PE})
                    , [date_prepa_exp] = CONVERT(datetime, '{self.measurementDateTime}', 21)-- start date prépa expédition
                    , [time_prepa_exp] = CONVERT(datetime, '{self.measurementDateTime}', 21)-- start time prépa expédition 
                where numblf='{numblf}'
                    --end-sql
                """
            return self.executeSql(sql=sql)
    def expedition(self, numblf='', userId=''):
        self.getDateUpdate()
        check = self.check_avant_expedition(nblf=numblf, table_name=self.table_name)
        if  check['exit'] ==  False:
            print('IMPOSSIBLE DE PASSE ICI !')
            return False
        elif check['exit'] == True:
            sql = f""" --begin-sql
            update
                    {self.table_name}

                    set [resp_exp]  = {userId} --  responsable start
                    , [statut] = CONVERT(int, {self.Exp})
                    , [date_exp] = CONVERT(datetime, '{self.measurementDateTime}', 21)-- start date expédition 
                    , [time_exp] = CONVERT(datetime, '{self.measurementDateTime}', 21)-- start time expédition 
                where numblf='{numblf}'
                    --end-sql
                """
            return self.executeSql(sql=sql)
    def check_avant_debut_ramassage(self, nblf, table_name='[Commerciale].[dbo].[aya_magasin_tache_table]'):

        
        sql =f""" --begin-sql
            select numblf, statut from {table_name} 
            
            where 
                numblf = '{nblf}'
                and statut = {self.BeforeDR} or statut is NULL
            --end-sql
        """
        return self.getChecked(sql)

    # Forcement Début Ramassage {self.DR} a été établi
    def check_avant_fin_ramassage(self, nblf, table_name='[Commerciale].[dbo].[aya_magasin_tache_table]'):

        sql =f""" --begin-sql
            select numblf, statut from {table_name} 
            where 
                numblf = '{nblf}'
            and statut = {self.DR}
            --end-sql
        """

        return self.getChecked(sql=sql)

    # Forcement FIN Ramassage {self.FR} a été établi
    def check_avant_debut_emballage(self, nblf, table_name='[Commerciale].[dbo].[aya_magasin_tache_table]'):

        sql =f""" --begin-sql
            select  numblf, statut  from {table_name} 
            where 
                numblf = '{nblf}'
            and statut = {self.FR}
            --end-sql
        """

        print(sql)

        return self.getChecked(sql=sql)

    # Frorcement Début emballage {self.DEm} a été établi 
    def check_avant_fin_emballage(self, nblf, table_name='[Commerciale].[dbo].[aya_magasin_tache_table]'):
        sql =f""" --begin-sql
            select  numblf, statut  from {table_name} 
            where 
                numblf = '{nblf}'
            and statut = {self.DEm}
            --end-sql
        """

        return self.getChecked(sql=sql)

    #  Frorcement Fin emballage {self.FEm} a été établi 
    def check_avant_preparation_expedition(self, nblf, table_name='[Commerciale].[dbo].[aya_magasin_tache_table]'):

        sql =f""" --begin-sql
            select  numblf, statut  from {table_name} 
            where 
                numblf = '{nblf}'
            and statut = {self.FEm} -- 
            --end-sql
        """

        return self.getChecked(sql=sql)

    # Forcement ceci a été préparé par {self.PE}
    def check_avant_expedition(self, nblf, table_name='[Commerciale].[dbo].[aya_magasin_tache_table]'):
        sql =f""" --begin-sql
            select numblf, statut from {table_name} 
            where 
                numblf = '{nblf}'
            and statut = {self.PE} -- 
            --end-sql
        """
        return self.getChecked(sql=sql)

    def getList(self, sql):
        cursor =  self.cursor
        cursor.execute(sql)
        datas = cursor.fetchall()

        return datas

class UserRepository(Repository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def loginFromQrcode(self, userId):
        sql = f"""--begin-sql
            SELECT * FROM [Commerciale].[dbo].[Aya_Users]
            WHERE [ID] = '{userId}'
        --end-sql"""
        print(sql)
        return self.checked(sql=sql)
    

class SessionService:
    def __init__(self, session=''):
        self.session = session
        self.ip = ''
        self.key_id = f'{self.ip}-ID'
        self.key_name = f'{self.ip}-name'
        self.key_prenom = f'{self.ip}-prenom'
        self.key_profil = f'{self.ip}-profil'

    def setIp(self, ip):
        self.ip =  ip
        print('IP =', self.ip)

    def getIp(self):
        return self.ip

    def updateKeys(self):
        self.key_id = f'{self.ip}-ID'
        self.key_name = f'{self.ip}-name'
        self.key_prenom = f'{self.ip}-prenom'
        self.key_profil = f'{self.ip}-profil'

    def getId(self):
        return self.key_id

    def checked (self):
        id      = True if self.key_id in self.session and self.session[self.key_id] is not None else False
        name    = True if self.key_name in self.session and self.session[self.key_name] is not None else False
        prenom  = True if self.key_prenom in self.session and self.session[self.key_prenom] is not None  else False
        profil  = True if self.key_profil in self.session and self.session[self.key_profil] is not None  else False
        chk = True if id and name and prenom and profil else False
        return chk

    def delete(self):
        sessionIp = str(self.key_id).replace('-ID', '')
        print('--------------------------------------------------')
        print(self.session)
        print('IP ID => ', str(self.key_id))
        print('SESSION => ', sessionIp)
        print('Session From request ',  self.ip)
        print('--------------------------------------------------')
        if self.checked(): # si c'est bien l'utilisateur qui a été spécifier si non ne fait rien
            if sessionIp != self.ip:
                return
            self.deleteAllHasSameIpAddress()

    def deleteAllHasSameIpAddress(self):
        self.session[self.key_id]       = None
        self.session[self.key_name]     = None
        self.session[self.key_prenom]   = None
        self.session[self.key_profil]   = None
    def set(self, userChecked):
        self.session[self.key_id]       = userChecked.ID.strip()
        self.session[self.key_name]     = userChecked.Nom
        self.session[self.key_prenom]   = userChecked.Prenom
        self.session[self.key_profil]   = userChecked.Profil.strip()

    def get(self):
        if self.checked():
            return {
                'ID'        : self.session[self.key_id]
                ,'name'     : self.session[self.key_name]
                ,'prenom'   : self.session[self.key_prenom]
                ,'profil'   : self.session[self.key_profil]

            }
        else: 
            return {}
