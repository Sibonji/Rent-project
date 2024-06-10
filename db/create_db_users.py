import sqlite3 as sq
import psycopg2 as ps
import random

connection = sq.connect('users.db')
cursor = connection.cursor()

# drop_tb = '''
# DROP TABLE IF EXISTS pilot
# '''
# cursor.execute(drop_tb)
# connection.commit()


user_tb = '''
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL,
    user_pwd_hash TEXT NOT NULL,
    phone_number TEXT NOT NULL
)
'''
cursor.execute(user_tb)
connection.commit()

cursor.close()
connection.close()