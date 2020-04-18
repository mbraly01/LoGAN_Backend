import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from PIL import Image
import sys
sys.path.append('/home/mbraly/python-for-byte-academy/Final_Project/Website/models')
from brand import Brand
import connector
from loGan import run
import os.path
from os import path
import os
from flask_cors import CORS
from gallery import Gallery

app = Flask(__name__)
cors = CORS(app)



@app.route('/run', methods=['POST'])
def feed():
    print(request.get_json())
    data = request.get_json()
    brand = Brand(brand_name = data["brand_name"], industry = data["industry"])
    brand.prep_db()
    brand.make_file()
    run()
    return data

@app.route('/industries', methods=['GET'])
def industries():
    brand = Brand()
    industry_list = brand.get_industries()
    react_industry_list = []
    for i in industry_list:
        react_industry_list.append({"value": i, "label": i})
    return jsonify({"industry_list": react_industry_list})

@app.route('/addToGallery', methods=['POST'])
def addToGallery():
    data = request.get_json()
    print(data)
    gallery = Gallery()
    gallery.add_to_gallery(brand_name=data["name"], number=data["number"])
    return data

@app.route('/makeGallery', methods=['GET'])
def makeGallery():
    gallery = Gallery()
    names = gallery.make_gallery()
    print(names)
    return jsonify({"names": names})

@app.route('/downloadGallery', methods=['GET'])
def downloadGallery():
    gallery = Gallery()
    gallery.download_gallery()
    return jsonify({"complete":"yes"})
    
    

if __name__ == "__main__":
    app.run(debug=True)




