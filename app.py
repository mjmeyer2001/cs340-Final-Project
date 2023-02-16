from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from flask import send_from_directory
import os

app = Flask(__name__)

# Routes
@app.route('/')
def root():
    return render_template("index.html")

@app.route('/airlines')
def airlines():
    return render_template("airlines.html")

@app.route('/airlines_airports')
def airlines_airports():
    return render_template("airlines_airports.html")

@app.route('/airports')
def airports():
    return render_template("airports.html")

@app.route('/flights')
def flights():
    return render_template("flights.html")

@app.route('/planes')
def planes():
    return render_template("planes.html")

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 50259))
    app.run(port=port, debug=True)