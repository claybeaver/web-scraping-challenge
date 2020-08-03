import scrape_mars
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

# Setup connection to mongodb
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.missiontomars_db

@app.route("/")
def home():
    homepage = mongo.db.collection.find_one()
    return render_template("index.html", homepage=homepage)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)