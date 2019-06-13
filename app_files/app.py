import os
import psycopg2
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template, json, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import json
from bson import ObjectId
from collections import OrderedDict


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
wine_opt1=db.wine_rating # creating/reading collection by option 1
wine_opt2=db.wine_history # creating/reading collection by option 2  
wine_opt2_list=db.wine_history_list # creating/reading collection by option 2  

func = lambda s: s[:1].lower() + s[1:] if s else '' #function to return lower case of all character of a strign

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api_rating")
def idata():
    wd=wine_opt1.find({},{'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(rows)

@app.route("/api_history")
def jdata():
    wd=wine_opt2.find({},{'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)
    return jsonify(rows)

@app.route("/api_history/country=<country>")
def jdata_country(country):
    country=func(country).title()

    wd=wine_opt2.find({'country': country}, {'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(rows)

@app.route("/api_history/year=<year>")
def jdata_year(year):
    wd=wine_opt2.find({'year': year}, {'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(rows)

@app.route("/api_history/country=<country>&year=<int:year>")
def jdata_country_year(country='',year=''):
    country=func(country).title()
    if (year):
        print("contry and year")
        wd=wine_opt2.find({'country': country,'year': str(year)}, {'_id': False})
    else:
        print("only country")
        wd=wine_opt2.find({'country': country}, {'_id': False})

    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(rows)

@app.route("/api_history/startyear=<syear>&endyear=<eyear>")
def jdata_styear_enyear(syear,eyear):
    wd=wine_opt2.find({'$and':[
        {'year': {'$gte': syear}}, 
        {'year': {'$lte': eyear}}
        ]}, {'_id': False})

    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(rows)

@app.route("/api_history/country=<country>&startyear=<syear>&endyear=<eyear>")
def jdata_country_styear_enyear(country,syear,eyear):
    country=func(country).title()
    wd=wine_opt2.find({'$and':[
        {'year': {'$gte': syear}}, 
        {'year': {'$lte': eyear}},
        {'country': country}]}, {'_id': False})

    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(rows)

@app.route("/api_history/GeoJSON")
def jdata_geojson():
    wd=wine_opt2_list.find({},{'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
        "title": "Wine History by Pygeons",
        "status": 200,
        "count": len(rows)
        },
        "features": [
        {
            "type": "Feature",

            "geometry" : {
                "type": "Point",
                "coordinates": [d["coordinate"]["lon"], d["coordinate"]["lat"]],
            },

            "properties" : 
            {

              "country":d['country'],
              "year": d['year'],
              "Production":  d["Production"],
              "Production_capita": d["Production_capita"],
              "Export": d["Export"],
              "Import": d["Import"],
              "Consumption": d["Consumption"],
              "Consumption_capita": d["Consumption_capita"],
              "Population": d["Population"],     
            } 
        }  for d in rows]
    }
    return json.dumps(geojson)


@app.route("/api_history/GeoJSON/country=<country>")
def jdata_geojson_country(country):
    country=func(country).title()
    wd=wine_opt2_list.find({'country': country}, {'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
        "title": "Wine History by Pygeons",
        "status": 200,
        "count": len(rows)
        },
        "features": [
        {
            "type": "Feature",

            "geometry" : {
                "type": "Point",
                "coordinates": [d["coordinate"]["lon"], d["coordinate"]["lat"]],
            },

            "properties" : 
            {

              "country":d['country'],
              "year": d['year'],
              "Production":  d["Production"],
              "Production_capita": d["Production_capita"],
              "Export": d["Export"],
              "Import": d["Import"],
              "Consumption": d["Consumption"],
              "Consumption_capita": d["Consumption_capita"],
              "Population": d["Population"],     
            } 
        }  for d in rows]
    }
    return json.dumps(geojson)



if __name__ == "__main__":
    app.run()





