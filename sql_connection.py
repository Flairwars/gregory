import pymysql
from decouple import config
class sql_class():
    def __init__(self): 
        host = "192.168.1.51"
        port = 3306
        user = config('SQLUSER')
        password = config('SQLPASS')
        database = config('SQLDATA')

        self.conn = pymysql.connect(host = host, port = port, user = user, password = password, database =database)
        self.cursor = self.conn.cursor()

    def get_user():
        pass
    