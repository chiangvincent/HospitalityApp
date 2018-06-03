from flask import Flask, render_template
from sqlalchemy import create_engine
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#
# engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Database123@localhost/hospitalityapp'
db = SQLAlchemy(app)


app.debug = True
db.init_app(app)

@app.route('/')
def home():
    from models import Hospitals
    a = Hospitals.query.filter_by(zipcode = '94538').first()
    return a.name;
    # return Hospitals;
    # return render_template('home.html')

# at the bottom to run the app
if __name__ == '__main__':
    # from sqlalchemy.orm import scoped_session, sessionmaker, Query
    # db_session = scoped_session(sessionmaker(bind=engine))
    # for item in db_session(Hospitals.zipcode, Hospitals.city):
    #     print (item)
    app.run()
