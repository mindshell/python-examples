import psycopg2
from webapp.globals import *

class DB(object):
    """Database handling class."""

    db_name = APP_DB_NAME
    db_user = "www"
    db_host = "localhost"
    db_port = APP_DB_PORT

    def __init__(self):
        # Connect to DB
        self.connection = None
        self.connect()

        # Create a cursor
        self.cursor = self.connection.cursor()

    def error(self, e, sql=None, bindvars=None):
        """Log database error."""

        logging.error("DB error!")
        logging.error(e)
        logging.error(type(e))
        if sql: logging.error(sql)
        if bindvars: logging.error(bindvars)

        if self.connection:
            self.connection.rollback()
            self.connection.close()
            self.connection = None

        if type(e) == psycopg2.OperationalError:
            raise WebsiteTooBusy, "Too many database connections requested!"
        else:
            raise

    def connect(self):
        """Connect to database."""

        try:
            self.connection = psycopg2.connect(dbname=DB.db_name, user=DB.db_user,
                                               host=DB.db_host, port=DB.db_port)

            self.connection.set_isolation_level(0)
        except Exception, e:
            self.error(e)

    def fetch_one(self, sql, *bindvars):
        """Fetch one row."""

        try:
            if not self.connection:
                self.connect()
                self.cursor = self.connection.cursor()

            self.cursor.execute(sql, bindvars)
            row = self.cursor.fetchone()

            return row
        except Exception, e:
            self.error(e, sql, bindvars)

    def fetch_all(self, sql, *bindvars):
        """Fetch all rows."""

        try:
            if not self.connection:
                self.connect()
                self.cursor = self.connection.cursor()

            self.cursor.execute(sql, bindvars)
            rows = self.cursor.fetchall()

            return rows
        except Exception, e:
            self.error(e, sql, bindvars)

    def execute(self, sql, *bindvars):
        """Execute query."""

        try:
            if not self.connection:
                self.connect()
                self.cursor = self.connection.cursor()

            self.cursor.execute(sql, bindvars)

            return
        except Exception, e:
            self.error(e, bindvars)

    def commit(self):
        """Commit any pending transaction to the database."""

        self.connection.commit()

        return

    def begin_trans(self):
        """Begin a database transaction."""

        sql = "BEGIN"
        self.execute(sql)

    def commit_trans(self):
        """Commit a database transaction."""

        sql = "COMMIT"
        self.execute(sql)
        self.commit()

    def disconnect(self):
        """Disconnect from database."""

        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except Exception, e:
                self.error(e)

    @staticmethod
    def escape(s):
        return s.replace('\'', '\'\'')

    @staticmethod
    def unescape(s):
        return s.replace('\'\'', '\'')
