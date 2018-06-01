from flask import Flask, render_template
from sqlalchemy import create_engine
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)

app.debug = True

@app.route('/')
def home():
    db = SQLAlchemy(app)
    db.init_app(app)
    db.create_all()
    return render_template('home.html')

class Hospitals(db.Model):
    __table__ = db.Model.metadata.tables['patientdata']
    def __repr__(self):
        return self.drg

# at the bottom to run the app
if __name__ == '__main__':
    # from sqlalchemy.orm import scoped_session, sessionmaker, Query
    # db_session = scoped_session(sessionmaker(bind=engine))
    # for item in db_session(Hospitals.zipcode, Hospitals.city):
    #     print (item)
    app.run()
