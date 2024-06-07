import sqlite3
from model.user import User


class Users:
    def __init__(self):
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chatId TEXT PRIMARY KEY,
            username TEXT,
            subscribeType TEXT DEFAULT 'default'
        )
        """)
        conn.commit()
        conn.close()

    def add_user(self, chatId, username):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute(f"""
        INSERT INTO users (chatId, username) VALUES ('{chatId}', '{username}');
        """)
        conn.commit()
        conn.close()

    def get_user_list(self):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT * FROM users
        """)
        rows = cur.fetchall()

        users = []
        for row in rows:
            users.append(User.get_from_db(row))

