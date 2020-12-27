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
    
    def add_user(self, username, color):
        '''
        adds a user to the database
        input: <str> username, <str> color
        output: None
        '''
        sql = 'INSERT INTO redditusers (`username`,`color`) VALUES (%s,%s)'
        
        self.conn.ping(reconnect=True)
        try:
            self.cursor.execute(sql, (username, color))
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))
    
    def user_exists(self, username):
        '''
        checks if a user has been added to the database before
        '''
        sql = 'SELECT username FROM redditusers WHERE username = %s'
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, username)
        username = self.cursor.fetchall()

        if username:
            return True
        return False