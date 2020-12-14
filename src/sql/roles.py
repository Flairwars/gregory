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
        
    def add_user(self, user_id, name, guild_id):
        '''
        docs go here but imn lazy
        '''
        sql = 'INSERT INTO users (`id`, `name`, `guild_id`) VALUES (%s,%s,%s)'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (user_id, name, guild_id))
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def get_user(self, user_id, guild_id):
        '''
        docs go here but imn lazy
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
        
    def add_role(self, role_id, name, guild_id):
        '''
        docs go here but imn lazy
        '''
        sql = 'INSERT INTO roles (`id`, `name`, `guild_id`) VALUES (%s,%s,%s)'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (role_id, name, guild_id))
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def get_roles(self):
        '''
        docs go here but imn lazy
        '''
        sql = "SELECT * FROM roles "

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data
        else:
            return []

    def update_role_name(self, role_id, name):
        '''
        docs go here but imn lazy
        '''
        sql = "UPDATE roles SET `name` = %s WHERE `id` = %s"
        
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (name, role_id))
            self.conn.commit()

        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def remove_role(self, role_id, guild_id):
        '''
        docs go here but imn lazy
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
        docs go here but imn lazy
        '''
        sql = "SELECT `role_id` FROM user_role WHERE `user_id` = %s AND `guild_id` = %s"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, (user_id, guild_id))
        data = self.cursor.fetchall()
        if data:
            data2 = []
            for n in data:
                data2.append(n[0])
            return data2
        else:
            return []
    
    def add_user_role(self, user_id, role_id, guild_id):
        '''
        docs go here but imn lazy
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
        docs go here but imn lazy
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
        docs go here but imn lazy
        '''
        sql = "SELECT * FROM guilds "

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data
        else:
            return []

    def update_guild_name(self, guild_id, name):
        '''
        docs go here but imn lazy
        '''
        sql = "UPDATE guilds SET `name` = %s WHERE `id` = %s"
        
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (name, guild_id))
            self.conn.commit()

        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def add_guild(self, guild_id, name):
        '''
        docs go here but imn lazy
        '''
        sql = 'INSERT INTO guilds (`id`, `name`) VALUES (%s,%s)'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (guild_id, name))
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def remove_guild(self, guild_id):
        '''
        docs go here but imn lazy
        '''
        sql = 'DELETE FROM guilds WHERE `id` = %s'

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, guild_id)
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))
            