import sqlite3

CONN = sqlite3.connect('db/main.db')
# CONNECTION

CURSOR = CONN.cursor()
# CURSOR --> agent in sql database