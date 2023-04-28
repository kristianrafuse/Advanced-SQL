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

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"WELCOME TO THE HOMEPAGE!<br/><br/>"
        f"Here are the available routes to peruse:<br/><br/>"
        f"Precipitation data available at: /api/v1.0/precipitation<br/><br/>"
        f"Station data available at: /api/v1.0/stations<br/><br/>"
        f"Temperature data available at: /api/v1.0/tobs<br/><br/>"
        f"INTERACTIVE! WOW!!<br/><br/>"
        f"Data available from your start date to end date!:/api/v1.0/<start>/<end><br/><br/>"
        f"Enter dates as yyyy-mm-dd like this:<br/><br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_datetime = datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_from_most_recent = most_recent_datetime - timedelta(days=365)

    data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_from_most_recent).all()
    print(data)
    session.close()

if __name__ == '__main__':
    app.run(debug=True)








# @app.route("/api/v1.0/stations")
# def stations():
#     session = Session(engine)

#     session.close()

# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     session = Session(engine)

#     session.close()

# @app.route("/api/v1.0/tobs")
# def tobs():
#     session = Session(engine)

#     session.close()

# @app.route("/api/v1.0/<start>")
# def start():
#     session = Session(engine)

#     session.close()

# @app.route("//api/v1.0/<start>/<end>")
# def startend():
#     session = Session(engine)

#     session.close()

# 1. /

    # Start at the homepage.

    # List all the available routes.

# 2.  /api/v1.0/precipitation

    # Convert the query results from your precipitation analysis
    # (i.e. retrieve only the last 12 months of data) to a dictionary
    # using date as the key and prcp as the value.

    # Return the JSON representation of your dictionary.

# 3. /api/v1.0/stations

    # Return a JSON list of stations from the dataset.

    # 4. /api/v1.0/tobs

    # Query the dates and temperature observations of the most-active station
    # for the previous year of data.

    # Return a JSON list of temperature observations for the previous year.

# 5. /api/v1.0/<start> and /api/v1.0/<start>/<end>

    # Return a JSON list of the minimum temperature, the average temperature,
    # and the maximum temperature for a specified start or start-end range.

    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater
    # than or equal to the start date.

    # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the
    # dates from the start date to the end date, inclusive

# Hints
    # Join the station and measurement tables for some of the queries.

    # Use the Flask jsonify function to convert your API data to a valid JSON response object.