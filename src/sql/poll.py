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

    def add_poll(self, message_id, channel_id, guild_id, name, time, emote_ids, args):
        '''
        Adds row to polls table
        Adds rows to poll options table
        input: <str> message_id, <str> channel_id, <str> guild_id, <str> name, <datetime> time, <list  int> emote_id, <list str> args
        output: none
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
            return str(data[0][0])
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))

    def toggle_vote(self, poll_id, guild_id, emote_id, user_id):
        """
        checks whether user exists
        adds user
        check if user has voted 
        adds user vote
        removes user vote
        input: <str> message_id, <str> channel_id, <str> guild_id, <str> emote_id, <str> user_id
        output: None, True, False
        """
        
        get_user = "SELECT id FROM users WHERE id = %s AND guild_id = %s"
        add_user = "INSERT INTO users (`id`, `guild_id`) VALUES (%s,%s)"

        get_vote = "SELECT user_id FROM votes WHERE poll_id = %s AND user_id = %s AND emote_id = %s"
        add_vote = "INSERT INTO votes (`poll_id`, `user_id`, `emote_id`) VALUES (%s,%s,%s)"
        delete_vote = "DELETE FROM votes WHERE poll_id = %s AND user_id = %s AND emote_id = %s"

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
        self.cursor.execute(get_vote, (poll_id, user_id, emote_id))
        voted = self.cursor.fetchall()
        if not voted:
            # adds vote
            try:
                self.cursor.execute(add_vote, (poll_id, user_id, emote_id))
                self.conn.commit()
                return True
            except  Exception as exc:
                    self.conn.rollback()
                    print(str(exc))
        else:
            # removes vote
            try:
                self.cursor.execute(delete_vote, (poll_id, user_id, emote_id))
                self.conn.commit()
                return False
            except  Exception as exc:
                    self.conn.rollback()
                    print(str(exc))
        return None
    
    def get_poll(self, message_id, channel_id, guild_id):
        '''
        gets the poll id from the polls db
        input: <str> message_id, <str> channel_id, <str> guild_id
        output: <int> id
        '''
        get_poll = "SELECT id FROM polls WHERE message_id = %s AND channel_id = %s AND guild_id = %s"

        self.conn.ping(reconnect=True)
        # get relevent poll
        self.cursor.execute(get_poll, (message_id, channel_id, guild_id))
        poll_id = self.cursor.fetchall()
        return poll_id[0][0]

    def check_polls(self, user_id):
        '''
        gets poll id from all the polls that someone as voted on
        input: <str> user_id
        output: <list int> poll_id
        '''
        sql = "SELECT polls.id FROM polls,votes WHERE votes.user_id = %s AND polls.id = votes.poll_id"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, user_id)
        data = self.cursor.fetchall()
        return data

    def check_votes(self, user_id, poll_id):
        '''
        checks how many votes are on a poll and reponds with the name of the option
        input: <str> user_id, <int> poll_id
        output: <list str> arg
        '''
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

    def get_poll_name(self, poll_id):
        '''
        gets the poll name from polls
        input: <int> poll_id
        output: <str> name
        '''
        sql = "SELECT name FROM polls WHERE id = %s"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, poll_id)
        data = self.cursor.fetchall()
        return data[0][0]

    def get_polls(self):
        '''
        gets all poll ids and times
        input: None
        output: <list int> poll_id, <list datetime> time
        '''
        sql = "SELECT id, time FROM polls"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
    
    def get_poll_info(self, poll_id):
        '''
        gets the name, channel and votes of a poll
        input: <int> poll_id
        output: <str> channel_id, <str> name, <list str> user_id, <list str> arg
        '''
        sql = "SELECT channel_id,name FROM polls WHERE id = %s"
        sql2 = """SELECT votes.user_id,poll_options.arg 
        FROM votes,poll_options 
        WHERE votes.poll_id = %s 
        AND poll_options.poll_id = votes.poll_id 
        AND votes.emote_id = poll_options.emote_id 
        """

        self.conn.ping(reconnect=True)

        self.cursor.execute(sql, poll_id)
        poll_info = self.cursor.fetchall()

        self.cursor.execute(sql2, poll_id)
        votes = self.cursor.fetchall()

        return poll_info[0], votes

    def remove_poll(self, poll_id):
        '''
        deletes poll from poll
        input: <str> poll_id
        output: None
        '''
        sql = "DELETE FROM polls WHERE id = %s"
        self.conn.ping(reconnect=True)

        try:
            self.cursor.execute(sql, poll_id)
            self.conn.commit()
        except  Exception as exc:
            self.conn.rollback()
            print(str(exc))
    
    def location_get_poll(self, message_id, channel_id, guild_id):
        '''
        gets poll via message location
        input: <str> message_id, <str> channel_id, <str> guild_id
        output: <int> id, <datetime> time
        '''
        sql = "SELECT id,time FROM polls WHERE message_id = %s AND channel_id = %s AND guild_id = %s"

        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, (message_id, channel_id, guild_id))
        poll_id = self.cursor.fetchall()
        return poll_id

###################################################

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