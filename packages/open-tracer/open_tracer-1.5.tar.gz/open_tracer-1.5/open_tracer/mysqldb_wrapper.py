"""
author: arun.rs
24th September 2018
"""
import MySQLdb
from trace import trace_resource
from datetime import datetime

class MySQLdbWrapper(object):
    """
    MySQLdb Library wrapper
    """
    def __init__(self, db_config, cursor_type=None):
        """
        :summary: Reads the credentials from
        :param db_config: DB Config credentials
        :param cursor_type: Cursor Type
        """
        self.cursor_type = None
        self.db_config = db_config
        self.connection_obj = None
        self.cursor_obj = None
        self.set_cursor(cursor_type)

    def connect(self):
        """
        :summary: Created a MySQL Connection
        :return: None
        """
        try:
            status = True
            start_time = datetime.now()
            self.connection_obj = MySQLdb.connect(
                                                   host=self.db_config['host'],
                                                   user=self.db_config['user'],
                                                   passwd=self.db_config['passwd'],
                                                   db=self.db_config['db'],
                                                   port=self.db_config['port'],
                                                   connect_timeout=self.db_config['connect_timeout'],
                                                   charset=self.db_config['charset']
                                                   )
        except Exception as e:
            status = False
            raise e
        finally:
            end_time = datetime.now()
            trace_resource("mysql", "Connecting", start_time, end_time, status)

    def set_cursor(self, cursor_type):
        """
        :summary: Set cursor with the requested cursor_type
        :param cursor_type: Cursor Type
        :return: None
        """
        if (not self.connection_obj):
            self.connect()
        if cursor_type == "tuple":
            self.cursor_obj = self.connection_obj.cursor()
        else:
            self.cursor_obj = self.connection_obj.cursor(MySQLdb.cursors.DictCursor)

    def processquery(self, query, count=0, args=None, fetch=True, returnprikey=0):
        """
        :summary: Executes the Mysql query and returns the results
        :param query: SQL raw query
        :param count: Number of records to be returned
        :param args: Arguments to be passed to the query
        :param fetch: Fetch the query result or not (True / False)
        :param returnprikey: Return primary key if 1
        :return: Query result
        """
        status = True
        start_time = datetime.now()
        try:
            self.cursor_obj.execute(query, args)
            if fetch:
                if count == 1:
                    return self.cursor_obj.fetchone()
                elif count > 1:
                    return self.cursor_obj.fetchmany(count)
                else:
                    return self.cursor_obj.fetchall()
            else:
                if returnprikey:
                    return self.cursor_obj.lastrowid
                else:
                    return self.cursor_obj.rowcount
        except Exception as e:
            status = False
            raise e
        finally:
            end_time = datetime.now()
            trace_resource("mysql", query, start_time, end_time, status)

    def save(self):
        """
        :summary: Commits the transactions
        :return: None
        """
        self.connection_obj.commit()

    def close(self):
        """
        :summary: Closes the MySQL connection
        :return:None

        """
        self.connection_obj.close()

    def revert(self):
        """
        :summary: Roll back the transactions
        :return:None
        """
        self.connection_obj.rollback()

    def __del__(self):
        """
        :summary: Closes the active connection once the scope of the object is over
        :return:None
        """
        self.close()