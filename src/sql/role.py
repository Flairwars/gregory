import sqlite3
from decouple import config
import pymysql


# noinspection SqlNoDataSourceInspection
class SqlClass:
    def __init__(self):
        self.database = 'datatables.db'

        sql_create_guilds_table = """CREATE TABLE IF NOT EXISTS guilds (
                                            guild_id integer PRIMARY KEY
                                        );"""
        sql_create_discord_users_table = """CREATE TABLE IF NOT EXISTS discord_users (
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
        sql_create_roles_table = """ CREATE TABLE IF NOT EXISTS roles (
                                            role_id integer,
                                            guild_id integer,
                                            FOREIGN KEY (guild_id) REFERENCES guilds (guild_id)
                                                ON DELETE CASCADE ON UPDATE CASCADE,
                                            PRIMARY KEY (role_id, guild_id)
                                        ); """
        sql_create_user_role_table = """ CREATE TABLE IF NOT EXISTS user_role (
                                            discord_id integer,
                                            role_id integer,
                                            guild_id integer,
                                            FOREIGN KEY (role_id, guild_id) REFERENCES roles (role_id, guild_id)
                                                ON UPDATE CASCADE ON DELETE CASCADE,
                                            FOREIGN KEY (discord_id, guild_id) REFERENCES user_guilds (discord_id, guild_id)
                                                ON UPDATE CASCADE ON DELETE CASCADE,
                                            PRIMARY KEY (discord_id, role_id, guild_id)
                                        ); """

        # create a database connection
        conn = self.create_connection(self.database)
        # create tables
        if conn is not None:
            conn.execute("PRAGMA foreign_keys = ON")
            self.create_table(conn, sql_create_guilds_table)
            self.create_table(conn, sql_create_discord_users_table)
            self.create_table(conn, sql_create_user_guilds_table)
            self.create_table(conn, sql_create_roles_table)
            self.create_table(conn, sql_create_user_role_table)
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
            # conn = sqlite3.connect(db_file)
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
        :param sql: the sql command being run
        :param parms: a list of tuples of information
        :return: any output from the sql code
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

    def get_roles(self, guild_id: int) -> list:
        """Gets a list of every role on a server
        :param guild_id:
        :return:
        """
        sql = """SELECT role_id FROM roles WHERE guild_id = ?"""
        return self.execute(sql, (guild_id,))

    def add_roles(self, guild_id: int, roles: list) -> None:
        """
        Adds multiple roles to the db
        :param guild_id: ID of server
        :param roles: A list of new roles
        :return:
        """
        sql = """INSERT INTO roles (`role_id`,`guild_id`) VALUES (?,?)"""
        parms = [(role, guild_id) for role in roles]
        self.execute_many(sql, parms)

    def remove_roles(self, guild_id: int, roles: list) -> None:
        """
        Removes multiple roles from the db
        :param guild_id: ID of server
        :param roles: A list of deleted roles
        :return:
        """
        sql = """DELETE FROM roles WHERE role_id = ? AND guild_id = ?"""
        parms = [(role, guild_id) for role in roles]
        self.execute_many(sql, parms)

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

    ############################################################

    def get_user_roles(self, discord_id: int, guild_id: int) -> list:
        """gets user roles from database
        :param discord_id: the users' id
        :param guild_id: the current guild od
        :return:
        """
        sql = """SELECT role_id FROM user_role WHERE discord_id=? AND guild_id=?"""
        return self.execute(sql, (discord_id, guild_id))

    def add_user_roles(self, discord_id: int, role_id: list, guild_id: int) -> None:
        """Adds user roles to database
        :param discord_id:
        :param role_id:
        :param guild_id:
        :return:
        """
        sql = """INSERT INTO user_role (`discord_id`, `role_id`, `guild_id`) VALUES (?,?,?)"""
        parms = [(discord_id, role, guild_id) for role in role_id]
        self.execute_many(sql, parms)

    def remove_user_roles(self, discord_id: int, guild_id: int) -> None:
        """Removes user roles from database
        :param discord_id:
        :param guild_id:
        :return:
        """
        sql = """DELETE FROM user_role WHERE `discord_id` = ? AND `guild_id` = ?"""
        self.execute(sql, (discord_id, guild_id))

    ############################################################

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
