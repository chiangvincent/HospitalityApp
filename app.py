from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return render_template('home.html')


# at the bottom to run the app
if __name__ == '__main__':
    app.run()
