import sqlite3
from sqlite3 import Error
import pandas as pd


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
    except Error as e:
        print(e)
    return conn


def select_table(conn, table):
    """ Query all rows in a table """
    cur = conn.cursor()
    query = "SELECT * FROM " + str(table)
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)


database = r"db_macae.db"
conn = create_connection(database)
df = pd.DataFrame({'name' : ['User 4', 'User 5']})
df.to_sql('users', con=conn, if_exists='replace')

HEADER_COLUNAS = [
    ('Nome do arquivo',(17,28)),
    ('Data de gravacao',(28,36)),
    ('Numero da remessa',(36,44))
]