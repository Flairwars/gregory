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

#######################################
        
    def add_user(self, user_id, guild_id):
        '''
        adds user to user table
        input: <str> user_id, <str> guild_id
        output: None
        '''
        sql = 'INSERT INTO users (`id`, `guild_id`) VALUES (%s,%s)'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (user_id, guild_id))
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def get_user(self, user_id, guild_id):
        '''
        gets user_id from users table
        input: <str> user_id, <str> guild_id
        output: <str> user_id
        '''
        sql = "SELECT id FROM users WHERE `id` = %s AND `guild_id` = %s"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, (user_id, guild_id))
        data = self.cursor.fetchall()
        if data:
            return data
        else:
            return None
#######################################
        
    def add_role(self, role_id, guild_id):
        '''
        adds role to roles table
        input: <str> role_id, <str> guild_id
        output: None
        '''
        sql = 'INSERT INTO roles (`id`, `guild_id`) VALUES (%s,%s)'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (role_id, guild_id))
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def get_roles(self):
        '''
        gets role_id from roles table
        input: <str> role_id, <str> guild_id
        output: <str> role_id
        '''
        sql = "SELECT * FROM roles WHERE guild_id = %s"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data
        else:
            return []

    def remove_role(self, role_id, guild_id):
        '''
        deletes role from roles table
        input: <str> role_id, <str> guild_id
        output: None
        '''
        sql = 'DELETE FROM roles WHERE `id` = %s AND `guild_id` = %s'
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (role_id, guild_id))
            self.conn.commit()

        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

#######################################

    def get_user_role(self, user_id, guild_id):
        '''
        gets role_id from roles table
        input: <str> role_id, <str> guild_id
        output: <str> role_id
        '''
        sql = "SELECT `role_id` FROM user_role WHERE `user_id` = %s AND `guild_id` = %s"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, (user_id, guild_id))
        data = self.cursor.fetchall()
        if data:
            return data
        else:
            return []
    
    def add_user_role(self, user_id, role_id, guild_id):
        '''
        adds row to user_role table
        input: <str> user_id, <str> role_id, <str> guild_id
        output: None
        '''
        sql = 'INSERT INTO user_role (`user_id`, `role_id`, `guild_id`) VALUES (%s,%s,%s)'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (user_id, role_id, guild_id))
            self.conn.commit()

        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))


    def remove_user_roles(self, user_id, guild_id):
        '''
        deletes user's roles from user_role table
        input: <str> user_id, <str> guild_id
        output: None
        '''
        sql = 'DELETE FROM user_role WHERE `user_id` = %s AND `guild_id` = %s'
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (user_id, guild_id))
            self.conn.commit()

        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))
#######################################

    def get_guilds(self):
        '''
        gets ids from guilds table
        input: None
        output: <str> guild_id
        '''
        sql = "SELECT id FROM guilds"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data
        else:
            return []

    def add_guild(self, guild_id):
        '''
        adds row to guilds table
        input: <str> guild_id
        output: <str> None
        '''
        sql = 'INSERT INTO guilds (`id`) VALUES (%s)'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, guild_id)
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def remove_guild(self, guild_id):
        '''
        deletes row to guilds table
        input: <str> guild_id
        output: <str> None
        '''
        sql = 'DELETE FROM guilds WHERE `id` = %s'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, guild_id)
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))
            