# Import the dependencies.

import sqlalchemy
 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/'2010-01-01'<br/>"
        f"/api/v1.0/daterange/'2010-09-15'/'2010-09-17'"
    )

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # query active station for the past 12 months
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#List of Station Names

@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

#List of Precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation for the last 12 months"""
    
    # Calculate the date one year from the last date in data set.
    yr_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date == yr_prior).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precip_info = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precip"] = prcp
        
        all_precip_info.append(precipitation_dict)

    return jsonify(all_precip_info)  

# Perform a query to retrieve info greater than or equal to specified date

@app.route("/api/v1.0/start/<startdate>")
def start(startdate):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), \
                            func.avg(Measurement.tobs)).filter(Measurement.date >= startdate).all()
    
    print(results)
    session.close()

        
    all_startdate_info = []
    for min, max, avg in results:
        startdate_dict={}
        startdate_dict["min temp"] = min
        startdate_dict["max temp"] = max
        startdate_dict["avg temp"] = avg
        
        all_startdate_info.append(startdate_dict)

    return jsonify(all_startdate_info)

# Perform a query to retrieve info greater than or equal to specified date range

@app.route("/api/v1.0/daterange/<startdate>/<enddate>")
def daterange(startdate, enddate):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), \
                            func.avg(Measurement.tobs)).filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all()
    
    session.close()

        
    all_daterange_info = []
    for min, max, avg in results:
        daterange_dict={}
        daterange_dict["min temp"] = min
        daterange_dict["max temp"] = max
        daterange_dict["avg temp"] = avg
        
        all_daterange_info.append(daterange_dict)

    return jsonify(all_daterange_info)
    
if __name__ == '__main__':
    app.run(debug=True)