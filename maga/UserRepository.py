from datetime import datetime
from maga.Repository import Repository

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
    

    def register(self, _name='', _prename='', _password=''):
        
        sql =f"""
            insert into dbo.Aya_user
            (name, prename, [password]) values('{_name}', '{_prename}','{_password}')
        """

        return self.executeSql(sql=sql)