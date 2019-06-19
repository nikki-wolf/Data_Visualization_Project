import os
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
wine_rating_list_World=db.wine_rating_list_World # reading wine rating and price collection for all the producing countries including US
wine_rating_list_States=db.wine_rating_list_States # reading wine rating and price collection for The producing States

func = lambda s: s[:1].lower() + s[1:] if s else '' #function to return lower case of all character of a strign

app = Flask(__name__)
FlaskJSON(app) #initiate FLASK-JSON


@app.route("/")
def home():
    return render_template("index.html")

# Route to return wine price, rating for all producing coutnries Worldwide in JSON format
@app.route("/api_rating")
def idata():
    country=request.args.get('country')
    if (country): 
        print("!!!!country=",country)
        country=func(country).title()
        wd=wine_rating_list_World.find({'Country':country},{'_id': False})
    else:
        wd=wine_rating_list_World.find({},{'_id': False})

    rows=[]
    for data in wd:
        rows.append(data)

    return jsonify(rows)

# Route to return wine price, rating for all the producing States in JSON format
# user can make a query by State, e.g. State=Texas
@app.route("/api_rating/States")
def idata_state():
    state=request.args.get('state')
    if (state): 
        print("!!!!state=",state)
        state=func(state).title()
        wd=wine_rating_list_States.find({'State':state},{'_id': False})
    else:
        wd=wine_rating_list_States.find({},{'_id': False})

    rows=[]
    for data in wd:
        rows.append(data)
    return jsonify(rows)

# Route to return wine price, rating data for all producing countries worldwide in GeoJSON format. User can add country as an argument
# e.g., /GeoJSON?country=frANCE
@app.route("/api_rating/GeoJSON")
def idata_geojson_country():
    country=request.args.get('country')
    if (country):
        if country !='US':
            country=func(country).title()
        wd=wine_rating_list_World.find({'Country': country}, {'_id': False})
    else:
        wd=wine_rating_list_World.find({}, {'_id': False})
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
              "Country":d["Country"],
              "Province": d["Province"],
              "Price":  d["Price"],
              "Rating": d["Rating"],
              "Variety": d["Variety"],
              "Subvariety": d["Subvariety"], 
            } 
        }  for d in rows]
    }
    return json.dumps(geojson)

# Route to return wine price, rating data for all producing countries worldwide in GeoJSON format. User can add country as an argument
# e.g., /GeoJSON?country=frANCE

@app.route("/api_rating/States/GeoJSON")
def idata_geojson_state():
    state=request.args.get('state')
    if (state):
        state=func(state).title()
        wd=wine_rating_list_States.find({'State': state}, {'_id': False})
    else:
        wd=wine_rating_list_States.find({}, {'_id': False})
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
              "Country":d["Country"],
              "State":d['State'],
              "Price":  d["Price"],
              "Rating": d["Rating"],
              "Variety": d["Variety"],
              "Subvariety": d["Subvariety"], 
            } 
        }  for d in rows]
    }
    return json.dumps(geojson)




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
        wd=wine_history_list.find({'Country': country}, {'_id': False})
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
                "coordinates": [d["Coordinate"]["lon"], d["Coordinate"]["lat"]],
            },

            "properties" : 
            {
              "Country":d['Country'],
              "Year": d['Year'],
              "Production_volume":  d["Production_volume"],
              "Production_capita": d["Production_capita"],
              "Production_capita_GDP": d["Production_capita_GDP"],
              "Consumption_volume": d["Consumption_volume"],
              "Consumption_capita": d["Consumption_capita"],
              "Consumption_capita_GDP": d["Consumption_capita_GDP"],
              "Export_volume": d["Export_volume"],
              "Export_value": d["Export_value"],
              "Export_volume_GDP": d["Export_volume_GDP"],
              "Import_volume": d["Import_volume"],
              "Import_value": d["Import_value"],
              "Import_volume_GDP": d["Import_volume_GDP"],
              "Excess_volume":d["Excess_volume"],
              "Population": d["Population"],     
            } 
        }  for d in rows]
    }
    return json.dumps(geojson)



if __name__ == "__main__":
    app.run()





