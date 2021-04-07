import sqlite3
import datetime
import pymysql
from decouple import config


# noinspection SqlNoDataSourceInspection
class SqlClass:
    def __init__(self):
        self.database = 'datatables.db'
        sql_create_guilds_table = """CREATE TABLE IF NOT EXISTS guilds (
                                                    guild_id integer PRIMARY KEY
                                                );"""
        sql_create_users_table = """CREATE TABLE IF NOT EXISTS discord_users (
                                                    discord_id integer PRIMARY KEY
                                                );"""
        sql_create_user_guilds_table = """ CREATE TABLE IF NOT EXISTS user_guilds (
                                                    discord_id integer,
                                                    guild_id integer,
                                                    FOREIGN KEY (guild_id) REFERENCES guilds (guild_id)
                                                        ON DELETE CASCADE ON UPDATE CASCADE,
                                                    FOREIGN KEY (discord_id) REFERENCES discord_users (discord_id)
                                                        ON DELETE CASCADE ON UPDATE CASCADE,
                                                    PRIMARY KEY (discord_id, guild_id)
                                                ); """
        sql_create_polls_table = """CREATE TABLE IF NOT EXISTS polls (
                                            message_id integer,
                                            channel_id integer,
                                            guild_id integer,
                                            name text,
                                            time datetime,
                                            FOREIGN KEY (guild_id) REFERENCES guilds (guild_id)
                                                ON DELETE CASCADE ON UPDATE CASCADE,
                                            PRIMARY KEY (message_id, channel_id, guild_id)
                                        );"""
        sql_create_options_table = """ CREATE TABLE IF NOT EXISTS options (
                                            message_id integer,
                                            channel_id integer,
                                            guild_id integer,
                                            emote_id integer,
                                            name text,
                                            FOREIGN KEY (message_id, channel_id, guild_id)
                                                REFERENCES polls (message_id, channel_id, guild_id)
                                                ON DELETE CASCADE ON UPDATE CASCADE,
                                            PRIMARY KEY (emote_id, message_id, channel_id, guild_id)
                                        ); """
        sql_create_votes_table = """ CREATE TABLE IF NOT EXISTS votes (
                                            discord_id integer,
                                            emote_id integer,
                                            message_id integer,
                                            channel_id integer,
                                            guild_id integer,
                                            FOREIGN KEY (emote_id, message_id, channel_id, guild_id)
                                                REFERENCES options (emote_id, message_id, channel_id, guild_id)
                                                ON DELETE CASCADE ON UPDATE CASCADE,
                                            FOREIGN KEY (discord_id, guild_id) REFERENCES user_guilds (discord_id, guild_id)
                                                ON UPDATE CASCADE ON DELETE CASCADE,
                                            PRIMARY KEY (discord_id, emote_id, message_id, channel_id, guild_id)
                                        ); """

        # create a database connection
        conn = self.create_connection(self.database)
        # create tables
        if conn is not None:
            #conn.execute("PRAGMA foreign_keys = ON")
            self.create_table(conn, sql_create_guilds_table)
            self.create_table(conn, sql_create_users_table)
            self.create_table(conn, sql_create_user_guilds_table)
            self.create_table(conn, sql_create_polls_table)
            self.create_table(conn, sql_create_options_table)
            self.create_table(conn, sql_create_votes_table)
        else:
            print("Error! cannot create the database connection.")

    @staticmethod
    def create_connection(db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            # If you are testing and debugging, change which lines are commented out. you will have to do this for each sql file
            #conn = sqlite3.connect(db_file)
            conn = pymysql.connect(host=config('SQLIP'), port=int(config('SQLPORT')), user=config('SQLUSER'), password=config('SQLPASS'),
                                   database=config('SQLDATA'))
            return conn
        except Exception as e:
            print(e)

        return conn

    @staticmethod
    def create_table(conn, create_table_sql: str) -> None:
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Exception as e:
            print(e)

    def execute(self, sql: str, parms: tuple = ()) -> list:
        """Executes a single command
        :param sql:
        :param parms:
        :return:
        """
        conn = self.create_connection(self.database)

        if conn is not None:
            try:
                c = conn.cursor()
                c.execute(sql, parms)
                data = c.fetchall()
                conn.commit()
                return data
            except Exception as e:
                print(e)

    def execute_many(self, sql: str, parms: list) -> list:
        """Executes a multi line command
        :param sql:
        :param parms:
        :return:
        """
        conn = self.create_connection(self.database)

        if conn is not None:
            try:
                c = conn.cursor()
                c.executemany(sql, parms)
                data = c.fetchall()
                conn.commit()
                return data
            except Exception as e:
                print(e)

    ############################################################

    def get_guilds(self) -> list:
        """
        Gets all the guilds recorded on the discord bot
        :return: a tuple of all the discord server ids
        """
        sql = """SELECT guild_id FROM guilds"""
        return self.execute(sql)

    def add_guilds(self, guilds: list) -> None:
        """
        Adds multiple guilds to the db
        :param guilds: A list of new guilds
        :return:
        """
        sql = """INSERT INTO guilds (`guild_id`) VALUES (?)"""
        parms = [(guild, ) for guild in guilds]
        self.execute_many(sql, parms)

    def remove_guilds(self, guilds: list) -> None:
        """
        Remove multiple guilds to the db
        :param guilds: A list of old guilds
        :return:
        """
        sql = """DELETE FROM guilds WHERE guild_id = ?"""
        parms = [(guild, ) for guild in guilds]
        self.execute_many(sql, parms)

    def add_poll(self, message_id: int, channel_id: int, guild_id: int, name: str, time: datetime = None) -> None:
        """Creates a new poll
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :param name: the title of the poll
        :param time: optional time at which the poll ends
        :return:
        """
        sql = """INSERT INTO polls (`message_id`, `channel_id`, `guild_id`, `name`, `time`) VALUES (?,?,?,?,?)"""
        self.execute(sql, (message_id, channel_id, guild_id, name, time))

    def get_poll(self, message_id: int, channel_id: int, guild_id: int) -> list:
        """Selects message id of poll
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :return: the message id of the poll
        """
        sql = """SELECT polls.name, options.name, options.emote_id, polls.message_id, polls.channel_id, polls.guild_id
        FROM polls, options
        WHERE polls.message_id=? AND polls.channel_id=? AND polls.guild_id=?
        AND polls.message_id = options.message_id
        AND polls.channel_id = options.channel_id
        AND polls.guild_id = options.guild_id"""
        return self.execute(sql, (message_id, channel_id, guild_id))

    def get_polls(self):
        """Selects all polls in the database for setup
        :return: poll id and time
        """
        sql = """SELECT time, message_id, channel_id, guild_id FROM polls"""
        return self.execute(sql, ())

    def get_poll_time(self, message_id: int, channel_id: int, guild_id: int) -> list:
        """Gets poll time
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :param message_id:
        :param channel_id:
        :param guild_id:
        :return:
        """
        sql = """SELECT time, message_id, channel_id, guild_id FROM polls
        WHERE message_id=? AND channel_id=? AND guild_id=?"""
        return self.execute(sql, (message_id, channel_id, guild_id))

    def remove_poll(self, message_id: int, channel_id: int, guild_id: int) -> None:
        """Deletes a poll
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :return:
        """
        sql = """DELETE FROM polls WHERE message_id=? AND channel_id=? AND guild_id=?"""
        self.execute(sql, (message_id, channel_id, guild_id))

    def add_options(self, message_id: int, channel_id: int, guild_id: int, emote_ids: list, names: list) -> None:
        """Creates all the options in the options table
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :param emote_ids: the emote of the poll
        :param names: the name of the option
        :return:
        """
        sql = """INSERT INTO options (`message_id`, `channel_id`, `guild_id`, `emote_id`, `name`) VALUES (?,?,?,?,?)"""
        parms = [(message_id, channel_id, guild_id, emote_ids[n], names[n]) for n in range(len(names))]
        self.execute_many(sql, parms)

    def add_user(self, discord_id: int, guild_id: int) -> None:
        """Adds user to database
        :param discord_id: the discord id of the user
        :param guild_id: the id of the current discord server
        :return:
        """
        sql = """INSERT OR IGNORE INTO discord_users (discord_id) VALUES (?)"""
        self.execute(sql, (discord_id,))
        sql = """INSERT OR IGNORE INTO user_guilds (discord_id,`guild_id`) VALUES (?,?)"""
        self.execute(sql, (discord_id, guild_id))

    def add_vote(self, discord_id: int, emote_id: str, message_id: int, channel_id: int, guild_id: int) -> None:
        """Adds a vote
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :param emote_id: the id of emote
        :param discord_id: the id of the user's account
        :return:
        """
        sql = """INSERT INTO votes (`discord_id`, `emote_id`, `message_id`, `channel_id`, `guild_id`) VALUES (?,?,?,?,?)"""
        self.execute(sql, (discord_id, emote_id, message_id, channel_id, guild_id))

    def remove_vote(self, discord_id: int, emote_id: str, message_id: int, channel_id: int, guild_id: int) -> None:
        """Deletes a vote
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :param emote_id: the id of emote
        :param discord_id: the id of the user's account
        :return:
        """
        sql = """DELETE FROM votes WHERE discord_id=? AND emote_id=? AND message_id=? AND channel_id=? AND guild_id=?"""
        self.execute(sql, (discord_id, emote_id, message_id, channel_id, guild_id))

    def check_vote(self, discord_id: int, emote_id: str, message_id: int, channel_id: int, guild_id: int) -> list:
        """checks if a vote exists
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :param emote_id: the id of emote
        :param discord_id: the id of the user's account
        :return: message id of the poll
        """
        sql = """SELECT message_id FROM votes
        WHERE votes.discord_id=? AND votes.emote_id=? AND votes.message_id=? AND votes.channel_id=? AND votes.guild_id=?"""
        return self.execute(sql, (discord_id, emote_id, message_id, channel_id, guild_id))

    def get_votes(self, message_id: int, channel_id: int, guild_id: int) -> list:
        """Gets all the votes of a specific poll
        :param message_id: the message id of the poll
        :param channel_id: the channel id of the poll
        :param guild_id: the guild that the poll is in
        :return:
        """
        sql = """SELECT votes.emote_id FROM votes
        WHERE votes.message_id=? AND votes.channel_id=? AND votes.guild_id=?"""
        return self.execute(sql, (message_id, channel_id, guild_id))

    def check_votes(self, discord_id: int, guild_id: int) -> list:
        """Returns the name of every poll that the user has voted on
        :param discord_id: the user id of the poll
        :param guild_id: the guild that the poll is in
        :return:
        """
        sql = """
        SELECT polls.message_id, polls.channel_id, polls.guild_id, options.emote_id, options.name, polls.name
        FROM votes, options, polls
        WHERE votes.discord_id = ? AND votes.guild_id = ?
        AND votes.emote_id = options.emote_id
        AND votes.message_id = options.message_id AND options.message_id = polls.message_id
        AND votes.channel_id = options.channel_id AND options.channel_id = polls.channel_id
        AND votes.guild_id = options.guild_id AND options.guild_id = polls.guild_id
        """
        return self.execute(sql, (discord_id, guild_id))
