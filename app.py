################# Import dependencies ################

from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

    # Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from sqlalchemy import and_


############# Create a SQL connection #################

#First we create connection to our database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station




#Define last 12months variable
last_12_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)

############# Starting with Flask ###############
#Create Flask app
app = Flask(__name__)

#Create 
@app.route("/")
#List all routes that are available.
def welcome():
    return(
        f'Welcome to Hawai weather checkout<br/>'
        f'Here you can take a look on weather to pick a best time for your trip<br/>'
        f'You may want to take a look on this routes: <br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start> <br/>'
        f'/api/v1.0/<start>/<end>'
    )


#In the first route I guess we present the first query I made on jupyter notebook which retrieves the las 12 months of data
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Start session
    session = Session(bind=engine) 
    #Start query which gave me date, precipitation and station
    points = [Measurement.date, Measurement.prcp, Measurement.station ]
    last_12_months_data = session.query(*points).filter(Measurement.date > f'{last_12_months}').order_by(Measurement.date)
    #End session
    session.close()
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    results = []
    for date, prcp, station in last_12_months_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_dict["station"] = station
        results.append(prcp_dict)
    
    return jsonify(results)

#Here they asks us for Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    session = Session(bind=engine)
    all_stations = session.query(Station.station, Station.name)
    session.close()

    results = []
    for station, name in all_stations:
        sta_dict = {}
        sta_dict["station"] = station
        sta_dict["name"] = name
        results.append(sta_dict)
    
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(bind=engine)
    #Query the dates and temperature observations of the most active station for the last year of data.
    #We know that the most active station in the last year was 'USC00519281'

    activ_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date > f'{last_12_months}').order_by(Measurement.date.desc()).all()

    session.close()
    #Return a JSON list of temperature observations (TOBS) for the previous year.
    last_12_months_tobs = []
    for date, tobs in activ_tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"]  = tobs
        last_12_months_tobs.append(tobs_dict)

    return jsonify(last_12_months_tobs)

 #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/<start>")
def one_date(start):
    session = Session(bind=engine)
    available_dates = session.query(Measurement.date)

    for date in available_dates:
        if start == date:
            results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date == start).order_by(Measurement.date).all()
            return jsonify(results)
        else:
           return jsonify({"error": f"There is no records for {start}"}), 404

    session.close()


@app.route("/api/v1.0/<start>/<end>")
def two_dates(start, end):

    start_d = dt.date(int(start))
    end_d = dt.date(int(end))
    session = Session(bind=engine)
    available_dates = session.query(Measurement.date)
    for date in available_dates:
        if start_d == date and end_d == date:
            results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(and_(Measurement.date == start_d, Measurement.date== end_d))
            return jsonify(results)

    session.close()
    return jsonify({"error": f'There is no rocords between {start_d} and {end_d}'}), 404
    


### Flask end-up
if __name__ == '__main__':
    app.run(debug=True)
