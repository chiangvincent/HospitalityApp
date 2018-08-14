from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from sqlalchemy import create_engine, inspect, Column, String, Integer, Float, MetaData, Table
from sqlalchemy.orm import mapper, relationship, sessionmaker, create_session, clear_mappers, session
from sqlalchemy.dialects.mysql import VARCHAR, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from gmaps import get_distance

db_url = "mysql://root:@Database123@localhost/hospitalityapp"
engine = create_engine(db_url)

Base = declarative_base()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Database123@localhost/hospitalityapp'
# db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class HospitalsDistance(object):
    def __init__(self, id, name, address, avg_covered, distance):
        self.id = id
        self.name = name
        self.address = address
        self.avg_covered = avg_covered
        self.distance = distance

#takes in the query object (that has been filtered for state and drg), and the address as a string (to use in gmaps API for distance calc)
def create_distance_table():
    columns = ["id", "name", "address", "avg_covered", "distance"]
    metadata = MetaData(bind=engine)
    dist_table = Table('HospitalsDistance', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('address', String),
        Column('avg_covered', DECIMAL(8,2)),
        Column('distance', DECIMAL(10, 2))
        )

    metadata.create_all()
    clear_mappers()
    mapper(HospitalsDistance, dist_table)
    session = create_session(bind = engine, autocommit=False, autoflush=True)
    return session

#this is the filtered hospitals class (should never be modified)
class Hospitals(db.Model):
    __table__ = db.Model.metadata.tables['patientdatafilteredtwo']
    def __repr__(self):
        return self.name

# create_table('filtered_hospitals',
#              Column('name', String(25)),
#              Column('address', String(100)),
#              Column('state', String(2)),
#              Column('avg_covered', Float),
#              Column('new', Integer, primary_key = True),
#              Column('drg', String(100)),
#              Column('distance', Integer))

#printing the models
# inspector = inspect(engine)
# for _t in inspector.get_table_names():
#     print(_t)
