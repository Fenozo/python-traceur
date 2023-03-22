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