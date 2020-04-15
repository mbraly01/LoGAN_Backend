import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, 'logan.db')

def schema(dbpath="logan.db"):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()

        sql = """CREATE TABLE logos (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name VARCHAR,
            industry VARCHAR
        );"""
        cur.execute(sql)

if __name__ == "__main__":
    schema()