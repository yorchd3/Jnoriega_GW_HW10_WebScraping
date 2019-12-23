import json
import pymongo
from flask import Flask, render_template, redirect, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/scrape")
def scrape():
    collection = mongo.db.mars
    mars_data = scrape_mars.scrape()

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html",mars=mars)

if __name__ == "__main__":
    app.run()