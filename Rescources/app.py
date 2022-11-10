import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Rescources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
measurement = Base.classes.measurement
station = Base.classes.station



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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )

@app.route("/api/v1.0/precipitation") 
def precipitation():
    
    session = Session(engine)
    maxDate = dt.date(2017, 8 ,23)
    one_year_ago = maxDate - dt.timedelta(days=365)

    past_temp = (session.query(measurement.date, measurement.prcp)
                .filter(measurement.date <= maxDate)
                .filter(measurement.date >= one_year_ago)
                .order_by   (measurement.date).all())
    
    session.close()
    
    pre = {date: prcp for date, prcp in past_temp}
    
    return jsonify(pre)
    
    

@app.route('/api/v1.0/stations')
def stations():

    session = Session(engine)
    stations_all = Session.query(station.name, station.station).all()

    temp_return = list(np.ravel(stations_all))
    
    session.close()
    
    return jsonify(temp_return)

    

@app.route('/api/v1.0/tobs') 
def tobs():  
    
    session = Session(engine)
    maxDate = dt.date(2017, 8 ,23)
    one_year_ago = maxDate - dt.timedelta(days=365)


    prevyear = (Session.query(measurement.tobs)
                .filter(measurement.station == 'USC00519281')
                .filter(measurement.date <= maxDate)
                .filter(measurement.date >= one_year_ago)
                .order_by(measurement.tobs).all())
    
    session.close()
    
    return jsonify(prevyear)
    
    

@app.route('/api/v1.0/<start>') 
def start(start=None):

    session = Session(engine)
    tobs_only = (session.query(measurement.tobs).filter(measurement.date.between(start, '2017-08-23')).all())
    
    tobs_df = pd.DataFrame(tobs_only)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    session.close()
    
    return jsonify(tavg, tmax, tmin)
    

@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):

    session = Session(engine)
    tobs_only = (session.query(measurement.tobs).filter(measurement.date.between(start, end)).all())
    
    tobs_df = pd.DataFrame(tobs_only)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    session.close()
    
    return jsonify(tavg, tmax, tmin)


if __name__ == '__main__':
    app.run(debug=True)

