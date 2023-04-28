import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
measurement = Base.classes.measurement
station = Base.classes.station

#initialize flask app
app = Flask(__name__)


# 1. / Start at the homepage. List all the available routes. Added some links based off what we learned in the html classes. 

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"WELCOME TO THE HOMEPAGE!<br/><br/>"
        f"Here are the available routes to peruse:<br/><br/>"
        f"Precipitation data available at: <a href='http://127.0.0.1:5000/api/v1.0/precipitation'>Precipitation Data</a><br/><br/>"
        f"Station data (id, station, name) available at: <a href='http://127.0.0.1:5000/api/v1.0/stations'>Station Data</a><br/><br/>"
        f"Temperature data for the most active station available at: <a href='http://127.0.0.1:5000/api/v1.0/tobs'>Temperature Data for Most Active Station</a><br/><br/>"
        f"INTERACTIVE! WOW!!<br/><br/>"
        f"Data available by selecting your start date!: <a href='http://127.0.0.1:5000/api/v1.0/'>Start Date Range Query</a><br/><br/>"
        f"Enter dates as yyyy-mm-dd like this:<br/><br/>"
        f"http://127.0.0.1:5000/api/v1.0/api/v1.0/yyyy-mm-dd<br/><br/>"
        f"Data available by selecting your start date and end date!: <a href='http://127.0.0.1:5000/api/v1.0'>Start Date and End Date Range Query</a><br/><br/>"
        f"Enter dates as yyyy-mm-dd like this:<br/><br/>"
        f"http://127.0.0.1:5000/api/v1.0/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/><br/>"
)

# 2. Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent_datetime = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_from_most_recent = most_recent_datetime - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_from_most_recent).all()
    session.close()

    output = []
    for date, prcp, in results: 
        data = {}
        data["date"] = date
        data["prcp"] = prcp
        output.append(data)

    return jsonify(output)

# 3. Return a JSON list of stations from the dataset. Added all the details from available columns

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.id, station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()

    stationdata = list(np.ravel(results))

    return jsonify(stationdata)

# 4. Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year. 
# Decided to include date and an f string printing the most active station.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent_datetime = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_from_most_recent = most_recent_datetime - dt.timedelta(days=365)

    station_counts = session.query(measurement.station, func.count(measurement.station))\
                        .group_by(measurement.station)\
                        .order_by(func.count(measurement.station).desc())\
                        .all()

    sel = [measurement.station, 
       func.min(measurement.tobs), 
       func.max(measurement.tobs), 
       func.avg(measurement.tobs)]

    session.query(*sel)\
    .filter(measurement.station == "USC00519281", measurement.date)\
    .group_by(measurement.station)\
    .order_by(measurement.station)\
    .all()

    sel = [measurement.tobs, measurement.date]

    temperature_data = session.query(*sel)\
    .filter(measurement.station == "USC00519281")\
    .filter(measurement.date >= one_year_from_most_recent).all()
    session.close()

    temp_data = list(np.ravel(temperature_data))

    return jsonify({
        'message': f'The most active station is:{station_counts[0]}. Details below:',
        'temperature_data': temp_data
    })

if __name__ == '__main__':
    app.run(debug=True)
