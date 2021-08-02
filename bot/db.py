# -*- coding: utf-8 -*-

import sqlite3


def ensure_connection(func):
    def decorator(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            result = func(conn, *args, **kwargs)
        return result
    return decorator


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute("DROP TABLE IF EXISTS users")

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id              INTEGER PRIMARY KEY,
        user_id                     STRING,
        lang                        STRING);
    """)

    conn.commit()


@ensure_connection
def add_user(conn, user_id, lang: str):
    c = conn.cursor()
    c.execute("INSERT INTO users(user_id, lang) VALUES (?, ?)", (user_id, lang))
    conn.commit()


@ensure_connection
def return_user_lang(conn, lang):
    c = conn.cursor()
    c.execute("SELECT lang FROM users WHERE user_id = ?", (lang,))
    all_results = c.fetchone()
    return all_results
