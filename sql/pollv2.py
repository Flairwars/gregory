import pymysql
from decouple import config
import datetime

class sql_class():
    def __init__(self): 
        host = config('SQLIP')
        port = int(config('SQLPORT'))
        user = config('SQLUSER')
        password = config('SQLPASS')
        database = config('SQLDATA')

        self.conn = pymysql.connect(host = host, port = port, user = user, password = password, database =database)
        self.cursor = self.conn.cursor()

    def add_poll(self, message_id, channel_id, guild_id, name, time, emote_ids, args):
        '''
        docs go here but imn lazy
        '''
        sql = "INSERT INTO polls (`message_id`, `channel_id`, `guild_id`, `name`, `time`) VALUES (%s,%s,%s,%s,%s)"
        sql2 = "SELECT LAST_INSERT_ID() FROM polls"
        sql3 = "INSERT INTO poll_options (`poll_id`, `emote_id`, `arg`) VALUES (%s,%s,%s)"

        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, (message_id, channel_id, guild_id, name, time))
            self.cursor.execute(sql2)
            data = self.cursor.fetchall()

            for count in range(len(args)):
                self.cursor.execute(sql3, (data[0][0], str(ord(emote_ids[count])), args[count]))
            self.conn.commit()

        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def vote_add(self, message_id, channel_id, guild_id, emote_id, user_id):
        """
        docs go here but imn lazy
        """
        sql = "SELECT id FROM polls WHERE message_id = %s AND channel_id = %s AND guild_id = %s"
        sql2 = "SELECT id FROM users WHERE id = %s AND guild_id = %s"
        sql3 = "INSERT INTO users (`id`, `guild_id`) VALUES (%s,%s)"
        sql4 = "SELECT id FROM poll_options WHERE poll_id = %s AND emote_id = %s"
        sql5 = "INSERT INTO votes (`poll_id`, `user_id`, `option_id`) VALUES (%s,%s,%s)"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, (message_id, channel_id, guild_id))
        poll_id = self.cursor.fetchall()
        if poll_id:
            if not self.cursor.execute(sql2, (user_id, guild_id)):
                try:
                    self.cursor.execute(sql3, (user_id, guild_id))
                    self.conn.commit()
                except  Exception as exc:
                    self.conn.rollback()
                    print(str(exc))
                    return None
            
            self.cursor.execute(sql4, (poll_id[0][0], emote_id))
            option_id = self.cursor.fetchall()
            if option_id:
                try:
                    self.cursor.execute(sql5, (poll_id[0][0], user_id, option_id[0][0]))
                    self.conn.commit()
                except  Exception as exc:
                        self.conn.rollback()
                        print(str(exc))
                        return None

    def vote_remove(self, message_id, channel_id, guild_id, emote_id, user_id):
        """
        docs go here but imn lazy
        """
        sql = "SELECT id FROM polls WHERE message_id = %s AND channel_id = %s AND guild_id = %s"
        sql2 = "SELECT id FROM users WHERE id = %s AND guild_id = %s"
        sql3 = "INSERT INTO users (`id`, `guild_id`) VALUES (%s,%s)"
        sql4 = "SELECT id FROM poll_options WHERE poll_id = %s AND emote_id = %s"
        sql5 = "DELETE FROM votes WHERE poll_id = %s AND user_id = %s AND option_id = %s"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, (message_id, channel_id, guild_id))
        poll_id = self.cursor.fetchall()
        if poll_id:
            if not self.cursor.execute(sql2, (user_id, guild_id)):
                try:
                    self.cursor.execute(sql3, (user_id, guild_id))
                    self.conn.commit()
                except  Exception as exc:
                    self.conn.rollback()
                    print(str(exc))
                    return None
            
            self.cursor.execute(sql4, (poll_id[0][0], emote_id))
            option_id = self.cursor.fetchall()
            if option_id:
                try:
                    self.cursor.execute(sql5, (poll_id[0][0], user_id, option_id[0][0]))
                    self.conn.commit()
                except  Exception as exc:
                        self.conn.rollback()
                        print(str(exc))
                        return None