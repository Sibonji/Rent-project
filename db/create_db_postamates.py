import sqlite3 as sq
import psycopg2 as ps
import random

connection = sq.connect('postamates.db')
cursor = connection.cursor()

# drop_tb = '''
# DROP TABLE IF EXISTS pilot
# '''
# cursor.execute(drop_tb)
# connection.commit()

postamate_tb = '''
CREATE TABLE IF NOT EXISTS postamate (
    postamate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    postamate_ip TEXT NOT NULL,
    postamate_loc TEXT NOT NULL
)
'''
cursor.execute(postamate_tb)
connection.commit()

door_tb = '''
CREATE TABLE IF NOT EXISTS door (
    postamate_id INTEGER,
    door_id INTEGER,
    item_status INTEGER,
    user_id INTEGER,
    taken_time DATETIME,
    item_name TEXT NOT NULL,
    item_link TEXT NOT NULL,
    item_img TEXT NOT NULL
)
'''
cursor.execute(door_tb)
connection.commit()
new_post = ["192.168.31.29", "Общежитие 14"]
post_insert = '''
INSERT INTO postamate (postamate_ip, postamate_loc) VALUES (?, ?);
'''
cursor.execute(post_insert, new_post)
connection.commit()

new_door = [1, 26, 1, 0, "1000-0-0 00:00:00", "ESP32 DEVKIT V1", "https://wiki.amperka.ru/products:esp32-wroom-wifi-devkit-v1", "https://wiki.amperka.ru/_media/products:esp32-wroom-wifi-devkit-v1:esp32-wroom-wifi-devkit-v1.1.jpg"]
door_insert = '''
INSERT INTO door (postamate_id, door_id, item_status, user_id, taken_time, item_name, item_link, item_img) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
'''
cursor.execute(door_insert, new_door)
connection.commit()

new_door = [1, 27, 1, 0, "1000-0-0 00:00:00", "Arduino UNO", "https://arduino.ru/Hardware/ArduinoBoardUno", "https://store.arduino.cc/cdn/shop/products/A000066_03.front_934x700.jpg?v=1629815860"]
door_insert = '''
INSERT INTO door (postamate_id, door_id, item_status, user_id, taken_time, item_name, item_link, item_img) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
'''
cursor.execute(door_insert, new_door)
connection.commit()

cursor.close()
connection.close()