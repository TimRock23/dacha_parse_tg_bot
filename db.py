import sqlite3

DB_NAME = 'dacha.db'


def db_connection(func):
    """
    Decorator for secure connection to sqlite using context manager.
    Creates connection to DB if not exist and returns it.
    """

    def wrapper(*args, **kwargs):
        with sqlite3.connect(DB_NAME) as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return wrapper


@db_connection
def _init_db(conn: sqlite3.Connection):
    """
    Initiate database with droping existing tables.
    """
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS user_category')
    cursor.execute('DROP TABLE IF EXISTS category')
    cursor.execute('DROP TABLE IF EXISTS user')

    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


if __name__ == '__main__':
    _init_db()
