Advanced SQL
-------

In this example, I used Python and SQLAlchemy to do a basic climate analysis and data exploration of a climate database. Specifically, I use SQLAlchemy ORM queries, Pandas, and Matplotlib to create visualizations for my findings.

Use the SQLAlchemy create_engine() function to connect to the SQLite database.
Use the SQLAlchemy automap_base() function to reflect tables into classes, and then save references to the classes named station and measurement.
Link Python to the database by creating a SQLAlchemy session.
Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.
Design a query to calculate the total number of stations in the dataset.
Design a query to find the most-active stations
Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
Design a query to get the previous 12 months of temperature observation (TOBS) data.

Part 2: A Basic Flask App
------
Here I design a simple Flask API based on the queries above, creating a variety of routes to handle the requests.

/api/v1.0/precipitation
Convert the query results from the precipitation analysis to a dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.

/api/v1.0/stations
Return a JSON list of stations from the dataset.

/api/v1.0/tobs
Query the dates and temperature observations of the most-active station for the previous year of data.
Return a JSON list of temperature observations for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
