import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    connex = None
    try:
        connex = sqlite3.connect(db_file)
        return connex
    except Error as e:
        print(e)
    return connex


def select_table(connex, table):
    """ Query all rows in a table """
    cur = connex.cursor()
    query = "SELECT * FROM " + str(table)
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def sql_fetch(connex):
    cursor_obj = connex.cursor()
    cursor_obj.execute('SELECT name from sqlite_master where type= "table"')
    print(cursor_obj.fetchall())


database = r"database_macae.db"
conn = create_connection(database)

sql_fetch(conn)