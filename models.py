from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from sqlalchemy import  create_engine, inspect, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
db_url = "mysql://root:@Database123@localhost/hospitalityapp"
engine = create_engine(db_url)

Base = declarative_base()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Database123@localhost/hospitalityapp'
# db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

#testing:a = Hospitals.query.filter(Hospitals.zipcode.startswith('94538')).all()

class Hospitals(db.Model):
    __table__ = db.Model.metadata.tables['patientdata']
    def __repr__(self):
        return self.name

class Filtered_Hospitals(Hospitals, Base):
    __tablename__ = "filteredhospitals"
