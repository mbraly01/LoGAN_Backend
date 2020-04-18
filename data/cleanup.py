import sqlite3
import csv
import re

with sqlite3.connect("logan2.db") as conn:
    cur = conn.cursor()


    sql = """SELECT * FROM logos;"""
    cur.execute(sql,)
    for row in cur:
        with open ("cleanup.csv", "a", newline='') as f_obj:
            writer = csv.writer(f_obj)
            i = row[2]
            if i != "''":
                if "Retail" in i or "retail" in i:
                    i = "Retail"
                elif "SaaS" in i:
                    i = "SaaS"
                elif "Real" in i or "real" in i:
                    i = "Real Estate"
                else:
                    j = re.findall(r"\w+|[^\w\s]", i, re.UNICODE)
                    if j == []:
                        k = re.findall('[A-Z][^A-Z]*', i)
                        if k == []:
                            j = i
                        else:
                            j = j[0]
                    else:
                        k = re.findall('[A-Z][^A-Z]*', j[0])
                        if k == []:
                            j = j[0]
                        else:
                            j = k[0]
                    i = j
                sql = f"""UPDATE logos SET industry="{i}" WHERE pk={row[0]}"""
                cursor = conn.cursor()
                cursor.execute(sql)                    
                    
        f_obj.close()
