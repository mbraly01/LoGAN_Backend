import sqlite3
import csv
import re
# like games
# manufactur
# software
# hardware
#  at ,
#  consulting
#  Retail
#  at second caps Caps
# at "and"
# at "&"
# at (
# at/
# at[
# at:
# at - 


with sqlite3.connect("logan2.db") as conn:
    cur = conn.cursor()


    sql = """SELECT * FROM logos;"""

    # sql = """SELECT DISTINCT industry FROM logos;"""
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
                # print(i[0])
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
                    

                # if i[0][0] == '"':
                #     print("wee")
                #     j = i[0].replace('"', '')
                #     i = (j[0],)
        f_obj.close()




# new_brands = []
# for logo in logos:
#     pk = logo[0]
#     brand = logo[1]
#     industry = logo[2]
#     new_brands.append([pk, brand, industry])

# for new_brand in new_brands:
#     for i in "&(/[:-":
#         if i in brand[2]:
#              = (brand[2].split(i))[0]
#             break

