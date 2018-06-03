from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Database123@localhost/hospitalityapp'
# db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

#testing:a = Hospitals.query.filter(Hospitals.zipcode.startswith('94538')).all()

class Hospitals(db.Model):
    __table__ = db.Model.metadata.tables['patientdata']
    def __repr__(self):
        return self.name
