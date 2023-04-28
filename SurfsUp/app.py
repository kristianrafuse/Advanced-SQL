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

        f"Data available by selecting your start date!: <a href='http://127.0.0.1:5000/api/v1.0/temp/2016-08-23'>Start Date Range Query</a><br/><br/>"

        f'For a specified start, returns the minimum, average, and maximum temperatures for all the dates greater than or equal to the start date.<br/><br/>'

        f"Data available by selecting your start date and end date!: <a href='http://127.0.0.1:5000/api/v1.0/temp/2016-08-23/2016-11-31'>Start Date and End Date Range Query</a><br/><br/>"

        f"For a specified start date and end date, returns the minimum, average, and maximum temperatures for the dates from the start date to the end date, inclusive."
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

    #get the most recent date from the measurement table the date one year prior to that date.

    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent_datetime = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_from_most_recent = most_recent_datetime - dt.timedelta(days=365)

    #queries the measurement table to get the count of measurements for each station in descending order

    station_counts = session.query(measurement.station, func.count(measurement.station))\
                        .group_by(measurement.station)\
                        .order_by(func.count(measurement.station).desc())\
                        .all()

    # Queries the measurement table to get the temperature observations for the most active station for the previous year of data.
    # The temperature data is stored in a list and returned as a JSON object.

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

@app.route("/api/v1.0/temp/<start>")
def temp_start(start):
    session = Session(engine)

    #select the min, max, and avg values as required from the measurement data

    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    #query for table for the data base on measurement.date based on start date variable as data

    temperature_data = session.query(*sel)\
        .filter(measurement.date >= start)\
        .all()

    session.close()

    #loop through the data and populate list to JSONIFY!

    temp_list = []
    for min_temp, avg_temp, max_temp in temperature_data:
        temp_dict = {}
        temp_dict["min_temp"] = min_temp
        temp_dict["avg_temp"] = avg_temp
        temp_dict["max_temp"] = max_temp
        temp_list.append(temp_dict)

    return jsonify(temp_list)

#same as above with additional filter on measurement.date based on end date variable

@app.route("/api/v1.0/temp/<start>/<end>")
def tempstartend(start, end=None):
    session = Session(engine)

    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    if end:
        temperature_data = session.query(*sel)\
            .filter(measurement.date >= start)\
            .filter(measurement.date <= end)\
            .all()
    else:
        temperature_data = session.query(*sel)\
            .filter(measurement.date >= start)\
            .all()

    session.close()

    temp_list = []
    for min_temp, avg_temp, max_temp in temperature_data:
        temp_dict = {}
        temp_dict["min_temp"] = min_temp
        temp_dict["avg_temp"] = avg_temp
        temp_dict["max_temp"] = max_temp
        temp_list.append(temp_dict)

    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)