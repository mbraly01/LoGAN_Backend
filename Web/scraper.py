from bs4 import BeautifulSoup
import requests
import csv
import time
from urllib import request
import boto3
import os
import paramiko
import sqlite3
import wikipedia
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}

LINKSPATH = '../data/links.csv'
'''

#Scrape 11236 pages for links to logos

counter = 0
while counter < 11237:
    page = requests.get(f'https://www.brandsoftheworld.com/logos/letter?page={counter}')

    time.sleep(1)
    soup = BeautifulSoup(page.content, 'html.parser')
    list_items = soup.find_all('li')
    data = []

#Write links to links.csv
    with open('links.csv','a') as f_obj:
        for list_item in list_items:
            link = list_item.find('a')
            if link is not None:
                if 'logos' in link.attrs['href']:
                    pass
                elif 'logo' in link.attrs['href']:
                    f_obj.write(link.attrs['href']+'\n')
    counter += 1

#Get image addresses from brandoftheworld
with open ('links.csv','r') as f_obj:
    for line in f_obj:
        line = "https://www.brandsoftheworld.com" + line
        response = request.urlopen(line)
        soup = BeautifulSoup(response, 'html.parser')
        image = soup.find_all('img')
'''

def get_page(span):
    url = f"https://en.wikipedia.org/wiki/{span}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return soup

def get_industry(soup):
    tbl = soup.find("table", {"class": "infobox vcard"})
    list_of_table_rows = tbl.findAll('tr')
    info = {}
    for tr in list_of_table_rows:

            th = tr.find("th")
            td = tr.find("td")
            if th is not None:
                innerText = ''
                for elem in td.recursiveChildGenerator():
                    if isinstance(elem, str):
                        innerText += elem.strip()
                    elif elem.name == 'br':
                        innerText += '\n'
                info[th.text] = innerText
    return str(info["Industry"])

#Creat client, resource and bucket for AWS interaction
s3_client = boto3.client("s3")
s3=boto3.resource("s3")
bucket = s3.Bucket(name="logala")

#Open and read links collection
with open(LINKSPATH, 'r') as f_obj:
    for line in f_obj:
        industry = ""

#Scrape websites for images and names
        try:
            response = request.urlopen(f'https://www.brandsoftheworld.com{line}')
            soup = BeautifulSoup(response, 'html.parser')

            line = line[6:]

            #Get names for database
            spans = soup.find_all('span')
            for span in spans:
                span = str(span)
                spans = span[12:-14]
                spans = spans.title()
                spans = spans.replace(" ", "_")
                break

            images = soup.find_all('div', class_='image')
            for image in images:
                try:
                    src = image.find('img')['src']
                    request.urlretrieve(src, f'{spans}.jpg')
                    s3_client.upload_file(f"/home/mbraly/python-for-byte-academy/Final_Project/Web/{spans}.jpg","logala",spans + ".jpg")
                    os.remove(f"/home/mbraly/python-for-byte-academy/Final_Project/Web/{spans}.jpg")
                except:
                    pass

    # importing modules
            
            if not spans[-2:].lower() == "co" and not spans[-3:].lower() == "inc":
                try:
                    soup = get_page(spans)
                    industry = get_industry(soup)
                except:
                    try:
                        soup = get_page(spans + "_Co")
                        industry = get_industry(soup)
                    except:
                        try:
                            soup = get_page(spans + "_Inc")
                            industry = get_industry(soup)
                        except:
                            pass
            elif span[-2:].lower() == "co":
                try:
                    soup = get_page(spans)
                    industry = get_industry(soup)
                except AttributeError:
                    pass
                span = span[:-2]

            elif span[-3:].lower == "inc":
                try:
                    soup = get_page(spans)
                    industry = get_industry(soup)
                except AttributeError:
                    pass

            with sqlite3.connect("logan.db") as conn:
                cur = conn.cursor()

                sql = """INSERT INTO logos 
                (brand_name, industry) VALUES (?,?);"""
                
                cur.execute(sql, (spans, industry))
            print(line)
        except:
            pass
