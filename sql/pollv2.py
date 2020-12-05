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
                self.cursor.execute(sql3, (data[0][0], emote_ids[count], args[count]))
            self.conn.commit()

        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

