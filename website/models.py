from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
import certifi


cluster = MongoClient("mongodb+srv://GianITS:ProjectITS33@clusterits.do6lt.mongodb.net", tlsCAFile=certifi.where())
db = cluster['search_recipes']
recipes_collection = db['recipes']

# PyMongo for upload and download image ---------------------------------------------------------------------
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://GianITS:ProjectITS33@clusterits.do6lt.mongodb.net/search_recipes?retryWrites=true&w=majority"
mongo = PyMongo(app, tlsCAFile=certifi.where())

class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients