import sqlite3

DBPATH = '../data/queue.db'

def schema(dbpath=DBPATH):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()

        sql = """CREATE TABLE queue (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        brand_name VARCHAR
        );"""

        cur.execute(sql)

if __name__ == "__main__":
    schema()