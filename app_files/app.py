import os
import psycopg2
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template,json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import json
from bson import ObjectId


import pymongo

mlab_ID={
    "_id": "heroku_stp5z9b7.pygeons",
    "user": "pygeons",
    "db": "heroku_stp5z9b7",
    "roles": [
        {
            "role": "dbOwner",
            "db": "heroku_stp5z9b7"
        }
    ],
    "pass":'pygeons2019'
}

conn_mlab='mongodb://{one}:{two}@ds231377.mlab.com:31377/{three}'.format(one=mlab_ID['user'], two=mlab_ID['pass'], three=mlab_ID['db'])

client = pymongo.MongoClient(conn_mlab)

#connect to database heroku_stp5z9b7
db = client.heroku_stp5z9b7

# create/read collections for options 1 and 2:
wine_opt1=db.wine # creating/reading collection by option 1
wine_opt2=db.wine_history # creating/reading collection by option 2   

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

#@app.route("/api")
@app.route("/api/country=<country>")
def jdata_country(country):
    #try:
    wd=wine_opt2.find({'country': country}, {'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    #json_rows=json.dumps(rows)
#except Exception ,e:
#    print str(e)

    return jsonify(rows)

@app.route("/api/year=<year>")
def jdata_year(year):
    #try:
    wd=wine_opt2.find({'year': year}, {'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    #json_rows=json.dumps(rows)
#except Exception ,e:
#    print str(e)

    return jsonify(rows)
    
@app.route("/api/country=<country>&year=<year>")
def jdata_country_year(country,year):
    #try:
    wd=wine_opt2.find({'country': country,'year': year}, {'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    #json_rows=json.dumps(rows)
#except Exception ,e:
#    print str(e)

    return jsonify(rows)

@app.route("/api/year=<year>&country=<country>")
def jdata_year_country(country,year):
    #try:
    wd=wine_opt2.find({'country': country,'year': year}, {'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    #json_rows=json.dumps(rows)
#except Exception ,e:
#    print str(e)

    return jsonify(rows)

@app.route("/api/startyear=<syear>&endyear=<eyear>")
def jdata_styear_enyear(syear,eyear):
    #try:
    wd=wine_opt2.find({'$and':[
        {'year': {'$gte': syear}}, 
        {'year': {'$lte': eyear}}
        ]}, {'_id': False})

    rows=[]
    for data in wd:
        rows.append(data)

    #json_rows=json.dumps(rows)
#except Exception ,e:
#    print str(e)

    return jsonify(rows)

@app.route("/api/country=<country>&startyear=<syear>&endyear=<eyear>")
def jdata_country_styear_enyear(country,syear,eyear):
    #try:
    wd=wine_opt2.find({'$and':[
        {'year': {'$gte': syear}}, 
        {'year': {'$lte': eyear}},
        {'country': country}]}, {'_id': False})

    rows=[]
    for data in wd:
        rows.append(data)

    #json_rows=json.dumps(rows)
#except Exception ,e:
#    print str(e)

    return jsonify(rows)
#@app.route("/production")
#def production():
#    # return jsonify(df.to_json(orient="records"))
#    # return jsonify(df.to_json(orient="columns"))
#    return jsonify(production_df.to_json(orient="table"))

if __name__ == "__main__":
    app.run()





