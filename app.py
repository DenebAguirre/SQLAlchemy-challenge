################# Import dependencies ################
from flask import Flask


%matplotlib inline
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


############# Create a SQL connection #################

#Firs we create connection to our database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

############# Starting with Flask ###############
#Create Flask app
app = Flask(_name_)

#Create 
@app.route("/")
def welcome():
    return(
        f'Welcome to Hawai weather company'
        f'Here you can take a look on weather to pick a best time for your trip'
        f'You may want to take a look on this routes: '
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route("/api/v1.0/precipitation")
#Start session
session = Session(engine) 

points = [measurement.date, measurement.prcp, measurement.station ]
last_12_months_data = session.query(*points).filter(measurement.date > f'{last_12_months}').order_by(measurement.date)

#End session
session.close()


@app.route("/api/v1.0/stations")

@app.route("/api/v1.0/tobs")

@app.route("/api/v1.0/<start>")

@app.route("/api/v1.0/<start>/<end>")




### Flask end-up
if __name__ == '__main__':
    app.run(debug=True)
