import sqlite3
from typing import List

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
def add_user(conn: sqlite3.Connection, tg_id: int, username: str):
    """Insert user to user table."""
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user(id, username) values (?, ?)',
                   (tg_id, username))
    conn.commit()


@db_connection
def get_all_users_ids(conn: sqlite3.Connection) -> List[int]:
    """Returns list of all users."""
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM user')
    return [user[0] for user in cursor.fetchall()]


@db_connection
def is_user_exists(conn: sqlite3.Connection, tg_id: int) -> bool:
    """Checks is user exists. Returns Bool value."""
    cursor = conn.cursor()
    cursor.execute('SELECT EXISTS(SELECT 1 FROM user WHERE id = ?)',
                   (tg_id,))
    return True if cursor.fetchone()[0] else False


@db_connection
def get_category_id_by_name(conn: sqlite3.Connection, category: str) -> int:
    """Returns category_id by given name of category."""
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM category WHERE name = ?',
                   (category,))
    return cursor.fetchone()[0]


@db_connection
def add_user_category(conn: sqlite3.Connection, user_id: int, category: str):
    """Creates user-category relation."""
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO user_category(user_id, category_id) values (?, ?)',
        (user_id, get_category_id_by_name(category=category))
    )
    conn.commit()


@db_connection
def delete_user_category(conn: sqlite3.Connection,
                         user_id: int, category: str):
    """Delete user-category relation."""
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM user_category WHERE user_id = ? AND category_id = ?',
        (user_id, get_category_id_by_name(category=category))
    )
    conn.commit()


@db_connection
def get_user_categories(conn: sqlite3.Connection, user_id:int) -> List[str]:
    """Returns user following categories."""
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name FROM category INNER JOIN user_category ON '
        'category.id = user_category.category_id WHERE user_id = ?',
        (user_id,)
    )
    return [cat[0] for cat in cursor.fetchall()]


@db_connection
def get_all_categories(conn: sqlite3.Connection) -> List[str]:
    """Returns list of all categories."""
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM category')
    return [cat[0] for cat in cursor.fetchall()]


if __name__ == '__main__':
    _init_db()
