from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from sqlalchemy import  create_engine, inspect, Column, String, Integer, Float, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
db_url = "mysql://root:@Database123@localhost/hospitalityapp"
engine = create_engine(db_url)

Base = declarative_base()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Database123@localhost/hospitalityapp'
# db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

def create_table(name, *cols):
    meta = MetaData()
    meta.reflect(bind=engine)
    if name in meta.tables: return

    table = Table(name, meta, *cols)
    table.create(engine)

#this is the filtered hospitals class (should never be modified)
class Hospitals(db.Model):
    __table__ = db.Model.metadata.tables['patientdatafiltered']
    def __repr__(self):
        return self.name

create_table('filtered_hospitals',
             Column('name', String(25)),
             Column('address', String(100)),
             Column('state', String(2)),
             Column('avg_covered', Float),
             Column('new', Integer, primary_key = True),
             Column('drg', String(100)),
             Column('distance', Integer))

class FilteredHospitals(db.Model):
    __table__ = db.Model.metadata.tables['filtered_hospitals']
    def __repr__(self):
        return self.name

inspector = inspect(engine)
for _t in inspector.get_table_names():
    print(_t)
