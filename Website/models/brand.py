import boto3
import sqlite3
import sys
sys.path.append("/home/mbraly/python-for-byte-academy/Final_Project/Website/data")
import schema
import os
import numpy as np
from PIL import Image
import os.path
from os import path
import shutil


class Brand:

    FILEPATH = '/home/mbraly/python-for-byte-academy/Final_Project/Website/ifp/'
    DBPATH = "/home/mbraly/python-for-byte-academy/Final_Project/data/logan2.db"
    IMG_DBPATH = "/home/mbraly/python-for-byte-academy/Final_Project/Website/data/image_prep.db"
    IMAGE_SHAPE = (192, 192, 3)
    MAX_FILES = 1
    COUNTER_SIZE = 100
    MULTIPLIER = 5
    def __init__(self, brand_name="", industry=""):
        self.brand_name = brand_name
        self.industry = industry


    @classmethod
    def get_industries(cls):
        industry_list = []
        with sqlite3.connect(cls.DBPATH) as conn:
            cur = conn.cursor()

            sql = """SELECT DISTINCT industry FROM logos WHERE
            industry IS NOT '';"""
            cur.execute(sql,)
            data = cur.fetchall()
            for i in data:
                industry_list.append(i[0])
            return industry_list

    def prep_db(self):
        print("runs 1")
        counter = 1
        while counter < 10:
            shutil.copyfile('/home/mbraly/python-for-byte-academy/Final_Project/Website/matapp/my-app/src/output/placeholder.jpg', f'/home/mbraly/python-for-byte-academy/Final_Project/Website/matapp/my-app/src/output/img{counter}.jpg')
            counter += 1
        name_counter = 0
        counter = 0
        schema.schema()
        name_sim = []
        industry_sim = []
        while name_counter < len(self.brand_name) - 2:
            with sqlite3.connect(self.DBPATH) as conn:
                cur = conn.cursor()
                sql = """SELECT brand_name 
                FROM logos WHERE brand_name 
                LIKE '%{}%';""".format(self.brand_name[name_counter: name_counter + 2])
                cur.execute(sql,)
                name_sim = cur.fetchall()
                name_counter += 1
                for i in name_sim:
                    with sqlite3.connect(self.IMG_DBPATH) as conn:
                        cur = conn.cursor()
                        sql = """INSERT INTO brands (brand_name)
                        VALUES (?);"""

                        try:
                            for j in range(1):
                                cur.execute(sql, (i[0],))
                                counter += 1
                        except sqlite3.IntegrityError:
                            pass

        if self.industry != "":
            with sqlite3.connect(self.DBPATH) as conn:
                cur = conn.cursor()
                sql = """SELECT brand_name, industry 
                FROM logos WHERE industry LIKE '%{}%';""".format(self.industry)
                cur.execute(sql,)
                industry_sim = cur.fetchall()

                for i in industry_sim:
                    with sqlite3.connect(self.IMG_DBPATH) as conn:
                        cur = conn.cursor()

                        sql = """INSERT INTO brands (brand_name)
                        VALUES (?)"""
                        try:
                            for j in range(self.MULTIPLIER):
                                cur.execute(sql, (i[0],))
                                counter += 1
                        except sqlite3.IntegrityError:
                            pass
        if counter < self.MAX_FILES:
            remaining_spots=self.MAX_FILES-counter 
            with sqlite3.connect(self.DBPATH) as conn:
                cur = conn.cursor()
                sql = """SELECT brand_name FROM logos
                ORDER BY RANDOM() LIMIT {};""".format(remaining_spots)

                cur.execute(sql,)
                rand = cur.fetchall()

                with sqlite3.connect(self.IMG_DBPATH) as conn:
                    cur = conn.cursor()
                    for i in rand:
                        sql = """INSERT INTO brands (brand_name)
                        VALUES (?);"""
                        cur.execute(sql, (i[0],))

        
    def make_file(self):
        print("runs 1.5")
        total_list = []
        training_data = []
        s3=boto3.resource("s3")
        s3_client = boto3.client("s3")
        with sqlite3.connect(self.IMG_DBPATH) as conn:
            cur = conn.cursor()

            sql = """SELECT * FROM brands;"""

            cur.execute(sql,)
            total_list = cur.fetchall()
        counter = 0
        for brand_name in total_list:
            try:
                s3.meta.client.download_file("logala",brand_name[0]+".jpg",self.FILEPATH+brand_name[0]+".jpg")
                path = os.path.join(self.FILEPATH, brand_name[0]+".jpg")
                image = Image.open(path).resize((self.IMAGE_SHAPE[0], self.IMAGE_SHAPE[1]), Image.ANTIALIAS)
                if image.mode != "RGB":
                    image.load()
                    background = Image.new("RGB", (self.IMAGE_SHAPE[0], self.IMAGE_SHAPE[1]), (255, 255, 255))
                    if image.mode == "RGBA":
                        background.paste(image, mask=image.split()[3])
                    else:
                        background.paste(image) 
                    background.save('1.jpg', 'JPEG', quality=80)
                    background = background.resize((self.IMAGE_SHAPE[0], self.IMAGE_SHAPE[1]), 3)
                    training_data.append(np.asarray(background))
                    os.remove("1.jpg")
                else:
                    training_data.append(np.asarray(image))
                os.remove(self.FILEPATH+brand_name[0]+".jpg")
            except:
                pass   

        os.remove(self.IMG_DBPATH)
        training_data = np.reshape(training_data, (-1, self.IMAGE_SHAPE[0], self.IMAGE_SHAPE[1], self.IMAGE_SHAPE[2]))
        
        np.save(self.FILEPATH+"ifp.npy", training_data)

