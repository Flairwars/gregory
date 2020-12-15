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

    def toggle_vote(self, message_id, channel_id, guild_id, emote_id, user_id):
        """
        docs go here but imn lazy
        """
        get_poll = "SELECT id FROM polls WHERE message_id = %s AND channel_id = %s AND guild_id = %s"
        get_user = "SELECT id FROM users WHERE id = %s AND guild_id = %s"
        add_user = "INSERT INTO users (`id`, `guild_id`) VALUES (%s,%s)"

        get_vote = "SELECT user_id FROM votes WHERE poll_id = %s AND user_id = %s AND emote_id = %s"
        add_vote = "INSERT INTO votes (`poll_id`, `user_id`, `emote_id`) VALUES (%s,%s,%s)"
        delete_vote = "DELETE FROM votes WHERE poll_id = %s AND user_id = %s AND emote_id = %s"

        self.conn.ping(reconnect=True)
        # get relevent poll
        self.cursor.execute(get_poll, (message_id, channel_id, guild_id))
        poll_id = self.cursor.fetchall()

        if poll_id:
            # check if user exists
            if not self.cursor.execute(get_user, (user_id, guild_id)):
                try:
                    self.cursor.execute(add_user, (user_id, guild_id))
                    self.conn.commit()
                except  Exception as exc:
                    self.conn.rollback()
                    print(str(exc))
                    return None

            # checks if person has voted
            self.cursor.execute(get_vote, (poll_id[0][0], user_id, emote_id))
            voted = self.cursor.fetchall()
            if not voted:
                # adds vote
                try:
                    self.cursor.execute(add_vote, (poll_id[0][0], user_id, emote_id))
                    self.conn.commit()
                    return True
                except  Exception as exc:
                        self.conn.rollback()
                        print(str(exc))
            else:
                # removes vote
                try:
                    self.cursor.execute(delete_vote, (poll_id[0][0], user_id, emote_id))
                    self.conn.commit()
                    return False
                except  Exception as exc:
                        self.conn.rollback()
                        print(str(exc))
        return None
    
    def check_polls(self, user_id):
        sql = "SELECT polls.id FROM polls,votes WHERE votes.user_id = %s AND polls.id = votes.poll_id"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, user_id)
        data = self.cursor.fetchall()
        return data

    def check_votes(self, user_id, poll_id):
        sql = """
        SELECT poll_options.`arg`, polls.`name`
        FROM poll_options,votes,polls
        WHERE votes.user_id = %s
        AND votes.poll_id = %s
        AND votes.emote_id = poll_options.emote_id
        AND votes.poll_id = poll_options.poll_id
        AND votes.poll_id = polls.id
        """

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, (user_id, poll_id))
        data = self.cursor.fetchall()
        return data

    def get_poll(self, poll_id):
        sql = "SELECT name FROM polls WHERE id = %s"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, poll_id)
        data = self.cursor.fetchall()
        return data[0][0]