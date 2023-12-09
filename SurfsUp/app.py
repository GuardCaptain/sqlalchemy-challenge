# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify



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

# Welcome route
@app.route("/")
def welcome():
    "List of all available routes"
    return (
        f"Available Routes: Format for date is YYYYMMDD <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    query = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= dt.datetime(2016, 8, 23)).\
            order_by(Measurement.date).all()

    session.close()

    # Create dictionary
    one_year_prcp = []
    for date, prcp in query:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp 
        one_year_prcp.append(prcp_dict)

    return jsonify(one_year_prcp) 

# Stations route
@app.route("/api/v1.0/stations")
def station():
    query_station = session.query(Station.station).filter(Station.station == Measurement.station).\
        group_by(Station.station).all()

    session.close()

# Put into a list
    all_stations = list(np.ravel(query_station))

    return jsonify(all_stations)

# Tobs route
@app.route("/api/v1.0/tobs")
def tob():
    tob_query = session.query(Measurement.date, Measurement.tobs).filter(Station.id == 7).\
    filter(Measurement.date >= dt.datetime(2016, 8, 23)).all()

    session.close()

# Put into a list    
    temp_list = []
    for date, temp in tob_query:
        temp_list.append(temp)

    return jsonify(temp_list)

# Start route
@app.route("/api/v1.0/<start_date>")
def starter(start_date):
    start_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
                 .filter(Station.station == Measurement.station).filter(Measurement.date >= dt.datetime.strptime(start_date,"%Y%m%d")).all()

    session.close()

# Put into a list
    all_temps = list(np.ravel(start_query))

    return jsonify(all_temps)

# Start-End route
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    start_end_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Station.station == Measurement.station).filter(Measurement.date >= dt.datetime.strptime(start, "%Y%m%d"))\
    .filter(Measurement.date <= dt.datetime.strptime(end, "%Y%m%d")).all()

    session.close()

# Put into a list
    list_temps = list(np.ravel(start_end_query))

    return jsonify(list_temps)


if __name__ == "__main__":
    app.run(debug=True)