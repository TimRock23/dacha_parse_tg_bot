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
    """Initiate database with dropping existing tables."""
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS user_category')
    cursor.execute('DROP TABLE IF EXISTS category')
    cursor.execute('DROP TABLE IF EXISTS user')

    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


@db_connection
def add_user(conn: sqlite3.Connection, tg_id, username):
    """Insert user to user table."""
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user(id, username) values (?, ?)',
                   (tg_id, username))
    conn.commit()


@db_connection
def get_category_id_by_name(conn: sqlite3.Connection, category):
    """Returns category_id by given name of category."""
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM category WHERE name = ?',
                   (category,))
    category_id = cursor.fetchone()
    return category_id


@db_connection
def add_user_category(conn: sqlite3.Connection, user_id, category):
    """Creates user-category relation."""
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO user_category(user_id, category_id) values (?, ?)',
        (user_id, get_category_id_by_name(category)))
    conn.commit()


@db_connection
def delete_user_category(conn: sqlite3.Connection, user_id, category):
    """Delete user-category relation."""
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM user_category WHERE user_id = ? AND category_id = ?',
        (user_id, get_category_id_by_name(category)))
    conn.commit()


if __name__ == '__main__':
    _init_db()
