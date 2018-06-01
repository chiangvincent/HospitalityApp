from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Database123@localhost/hospitalityapp'
db = SQLAlchemy(app)

app.debug = True

@app.route('/')
def home():
    return render_template('home.html')


# at the bottom to run the app
if __name__ == '__main__':
    app.run()
