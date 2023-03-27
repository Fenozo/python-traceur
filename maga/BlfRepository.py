from datetime import datetime
from maga.Repository import Repository
import pytz

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
            tz = pytz.timezone('Indian/Antananarivo')
            self.measurementDateTime = now(tz=tz).strftime(self.datetimeformat)


    def getDataList(self, userId='', table_name='[Commerciale].[dbo].[aya_magasin_tache_table]'):
        
        sql = f"""--begin-sql 
            select numblf, statut from {table_name}
            where 
            ([rs_ram] = {userId} or [rs_em] = {userId})
            and statut > 0
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
