import sqlite3


class SqlClass:
    def __init__(self):
        self.database = 'datatables.db'
        sql_create_discord_users_table = """ CREATE TABLE IF NOT EXISTS discord_users (
                                            discord_id integer,
                                            PRIMARY KEY (discord_id)
                                        ); """
        sql_create_reddit_users_table = """CREATE TABLE IF NOT EXISTS reddit_users (
                                            reddit_name text,
                                            color text,
                                            PRIMARY KEY (reddit_name)
                                        )"""
        sql_create_reddit_discord_table = """CREATE TABLE IF NOT EXISTS reddit_discord (
                                            reddit_name text,
                                            discord_id integer,
                                            FOREIGN KEY (reddit_name) REFERENCES reddit_users (reddit_name)
                                                ON DELETE CASCADE ON UPDATE CASCADE,
                                            FOREIGN KEY (discord_id) REFERENCES discord_users (discord_id)
                                                ON DELETE CASCADE ON UPDATE CASCADE,
                                            PRIMARY KEY (reddit_name, discord_id)
                                        )"""


        # create a database connection
        conn = self.create_connection(self.database)
        # create tables
        if conn is not None:
            conn.execute("PRAGMA foreign_keys = ON")
            self.create_table(conn, sql_create_discord_users_table)
            self.create_table(conn, sql_create_reddit_users_table)
            self.create_table(conn, sql_create_reddit_discord_table)
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
            conn = sqlite3.connect(db_file)
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

    def get_reddit_color(self, reddit_name: str) -> list:
        """Checks sql database for their color
        :param reddit_name: the user's reddit name
        :return: color
        """
        sql = """SELECT color FROM reddit_users WHERE reddit_name = ?"""
        return self.execute(sql, (reddit_name,))

    def add_discord_user(self, discord_id: int) -> None:
        """Adds new user to sql database
        :param discord_id:

        :return:
        """
        sql = """INSERT OR IGNORE INTO discord_users (`discord_id`) VALUES (?)"""
        self.execute(sql, (discord_id,))

    def add_reddit_user(self, reddit_name: str, color: str) -> None:
        """Adds new user to sql database
        :param discord_id:
        :param reddit_name:
        :param color:
        :return:
        """
        sql = """INSERT OR IGNORE INTO reddit_users (`reddit_name`, `color`) VALUES (?, ?)"""
        self.execute(sql, (reddit_name, color))

    def add_reddit_discord(self, discord_id: int, reddit_name: str) -> None:
        """Adds new user to sql database
        :param discord_id:
        :param reddit_name:
        :param color:
        :return:
        """
        sql = """INSERT OR IGNORE INTO reddit_discord (`reddit_name`, `discord_id`) VALUES (?, ?)"""
        self.execute(sql, (reddit_name, discord_id))
