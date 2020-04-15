import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, 'image_prep.db')

def schema(dbpath=DBPATH):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()

        sql = """CREATE TABLE brands (
        brand_name VARCHAR
        );"""

        cur.execute(sql)

if __name__ == "__main__":
    schema()