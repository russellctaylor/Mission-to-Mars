##Let's break down what this code is doing.

##The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
##The second line says we'll use PyMongo to interact with our Mongo database.
#The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

#need to tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Set Up App Routes
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#add the next route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

#update the database using
#.update_one(query_parameter, {"$set": data}, options)
if __name__ == "__main__":
   app.run()