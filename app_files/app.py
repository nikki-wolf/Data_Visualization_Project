import os
import ast
import psycopg2
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template, json, request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import json
from bson import ObjectId
from collections import OrderedDict
from datetime import datetime


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
wine_history_list=db.wine_history_list # reading wine history collection by option 2  
wine_rating_list=db.wine_rating_list_World # reading wine rating and price collection

func = lambda s: s[:1].lower() + s[1:] if s else '' #function to return lower case of all character of a strign

app = Flask(__name__)
FlaskJSON(app) #initiate FLASK-JSON

@app.route("/get_time")
def get_time2():
    now = datetime.utcnow()
    #return json_response(time=now)
    return jsonify(time=now)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api_rating")
def idata():
    wd=wine_rating_list.find({},{'_id': False})
    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(rows)

@app.route("/api_history")
def jsondata():
    country=request.args.get('country')
    year=request.args.get('year')
    syear=request.args.get('startyear')
    eyear=request.args.get('endyear')
    
    def wd_probe(country,year,syear,eyear):
        print("inside fund: country=",country,"year=",year,"syear=",syear,"eyear=",eyear)         
        if (country): 
            country=func(country).title()
            if (year):# user input country, year
                return wine_opt2.find({'country': country, 'year': year}, {'_id': False})
            else: 
                if (syear): 
                    if (eyear): #user input country, staryear, endyear
                        return wine_opt2.find({'$and':[
                            {'year': {'$gte': syear}}, 
                            {'year': {'$lte': eyear}},
                            {'country': country}]}, {'_id': False})
                    else: #user input country, staryear
                        return wine_opt2.find({'$and':[
                            {'year': {'$gte': syear}}, 
                            {'country': country}]}, {'_id': False})
                else:
                    if (eyear): #user input country, endyear
                        return wine_opt2.find({'$and':[
                            {'year': {'$lte': eyear}},
                            {'country': country}]}, {'_id': False})
                    else: #user input country
                        return wine_opt2.find({'country': country}, {'_id': False})
        else: 
            if (year):# user input year
                return wine_opt2.find({'year': year}, {'_id': False})
            else:                    
                if (syear): 
                    if (eyear): #user input staryear, endyear
                        return wine_opt2.find({'$and':[
                            {'year': {'$gte': syear}}, 
                            {'year': {'$lte': eyear}}]}, {'_id': False})
                    else: #user input staryear
                        return wine_opt2.find({'$and':[
                            {'year': {'$gte': syear}}]}, {'_id': False})
                else:
                    if (eyear): #user input endyear
                        return wine_opt2.find({'$and':[
                            {'year': {'$lte': eyear}}]}, {'_id': False})
                    else: #user input nothing
                        return wine_opt2.find({}, {'_id': False})
            
    wd = wd_probe(country,year,syear,eyear)
    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(features=rows)


# Route to return data in GeoJSON format. User can add country as an argument
# e.g., /GeoJSON?country=frANCE
@app.route("/api_history/GeoJSON")
def jdata_geojson_country():
    country=request.args.get('country')
    if (country):
        country=func(country).title()
        wd=wine_history_list.find({'country': country}, {'_id': False})
    else:
        wd=wine_history_list.find({}, {'_id': False})
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





