from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo   
import scrape_mars

# setting up connection
app=Flask(__name__)
conn=PyMongo(app, uri='mongodb://localhost:27017/mars_db')

# setting up route 
@app.route("/")
def index():
    mars=conn.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():

    mars=conn.db.mars 
    mars_info=scrape_mars.scrape()
    mars.update({},mars_info,upsert=True)

    return redirect("http://localhost:5000/", code=302)

if __name__=="__main__":
    app.run(debug=True)