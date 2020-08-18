from flask import Flask, jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, and_

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
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
    date = dt.datetime(2016, 8, 22)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date).all()
    session.close()

    all_observations = []
    for date, prcp in results:
        observation_dict = {}
        observation_dict[date] = prcp
        all_observations.append(observation_dict)
        
    return jsonify(all_observations)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    date = dt.datetime(2016, 8, 22)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > date).filter(Measurement.station == 'USC00519281').all()
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    
    sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    results = session.query(*sel).\
    filter(Measurement.date >= start).\
    group_by(Measurement.date).\
    all()
        
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    results = session.query(*sel).\
    filter(and_(Measurement.date >= start, Measurement.date <= end)).\
    group_by(Measurement.date).\
    all()
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

