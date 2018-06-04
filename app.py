from flask import Flask, render_template, request
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from sqlalchemy.ext.declarative import declarative_base
from gmaps import get_state, get_geocode


# engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)
#163065 = num rows of table
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Database123@localhost/hospitalityapp'
db = SQLAlchemy(app)


app.debug = True
db.init_app(app)

@app.route('/')
def home():
    from models import Hospitals
    return render_template('home.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        address = request.form['address']
        geocode = get_geocode(address)
        state = get_state(geocode)
        return state;

#returns top 3 closest hospitals from database
def find_closest(address):
    from models import Hospitals





# at the bottom to run the app
if __name__ == '__main__':
    # from sqlalchemy.orm import scoped_session, sessionmaker, Query
    # db_session = scoped_session(sessionmaker(bind=engine))
    # for item in db_session(Hospitals.zipcode, Hospitals.city):
    #     print (item)
    app.run()
