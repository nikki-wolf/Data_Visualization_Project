import os
import psycopg2
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import config

user = 'xiacnjvpghbmfr'
password = 'b3cf30fa5bf7debca00266a482ce7521d03a07f4ceea8e45b3bd6dd4d7e71951'
port = '5432'
database = 'dkkbr6cn2l5mv'
host = 'ec2-54-163-230-199.compute-1.amazonaws.com'
url = 'postgres://'+user+':'+password+'@'+host+':'+port+'/'+database

# url = config.url

engine = sqlalchemy.create_engine(url)

# inspector = inspect(engine)
# for table_name in inspector.get_table_names():
#    print(table_name)
#    for column in inspector.get_columns(table_name):
#        print("Column: %s" % column['name'])

production_df = pd.read_sql("SELECT * FROM production_db", engine)
consumption_df = pd.read_sql("SELECT * FROM consumption_db", engine)
population_df = pd.read_sql("SELECT * FROM population_db", engine)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/production")
def production():
    # return jsonify(df.to_json(orient="records"))
    # return jsonify(df.to_json(orient="columns"))
    return jsonify(production_df.to_json(orient="table"))

@app.route("/consumption")
def consumption():
    # return jsonify(df.to_json(orient="records"))
    # return jsonify(df.to_json(orient="columns"))
    return jsonify(consumption_df.to_json(orient="table"))

@app.route("/population")
def population():
    # return jsonify(df.to_json(orient="records"))
    # return jsonify(df.to_json(orient="columns"))
    return jsonify(population_df.to_json(orient="table"))

if __name__ == "__main__":
    app.run()





