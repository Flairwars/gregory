import pymysql
from decouple import config

class sql_class():
    def __init__(self): 
        host = config('SQLIP')
        port = int(config('SQLPORT'))
        user = config('SQLUSER')
        password = config('SQLPASS')
        database = config('SQLDATA')

        self.conn = pymysql.connect(host = host, port = port, user = user, password = password, database =database)
        self.cursor = self.conn.cursor()
    
    def get_user(self, username):
        '''
        gets the user's color from reddit_users table
        input: <str> username
        output: <str> color, None
        '''
        sql = 'SELECT color FROM redditusers WHERE username = %s'

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, username)
        color = self.cursor.fetchall()
        if color:
            return color[0][0]
        return None