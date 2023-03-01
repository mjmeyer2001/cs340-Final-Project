from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from flask import send_from_directory
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_meyermat'#'cs340_sosiakr'
app.config['MYSQL_PASSWORD'] = '9415'#'7270'
app.config['MYSQL_DB'] = 'cs340_meyermat'#cs340_sosiakr'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/airlines', methods=['POST', 'GET'])
def airlines():
    if request.method == 'GET':
        query = "SELECT airline_id, name FROM airlines ORDER BY airline_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airlines = cur.fetchall()

        return render_template(
            "airlines.j2",
            airlines=db_airlines)
    
    if request.method == 'POST':
        id = request.form["input-airline-id"]
        name = request.form["input-airline-name"]
        query = "INSERT INTO airlines (airline_id, name) VALUES (%s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (id, name))
        mysql.connection.commit()
        cur.close()
        return redirect('/airlines')

@app.route('/search_airlines', methods=['POST'])
def search_airlines():
    if request.method == 'POST':
        name = request.form["search-airline-name"]
        search_term = '{}%'.format(name)
        query = "SELECT airline_id, name FROM airlines WHERE name LIKE %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (name))
        search_results = cur.fetchall()

        return render_template(
            "airlines.j2",
            airlines=search_results
        )

@app.route('/delete_airline/<string:airline_id>')
def delete_airline(airline_id):
    query = "DELETE FROM airlines WHERE airline_id = '%s'" % (airline_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return redirect('/airlines')

@app.route('/update_airline/<string:airline_id>', methods=['POST', 'GET'])
def update_airline(airline_id):

    if request.method == 'GET':
        query = "SELECT airline_id, name FROM airlines WHERE airline_id = '%s'" % (airline_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airlines = cur.fetchone()
        cur.close()

        return render_template("forms/update_airlines.j2", airlines=db_airlines)

    if request.method == 'POST':
        input_airline_name = request.form['airline-name']

        query = "UPDATE airlines SET name = '%s' WHERE airline_id = '%s'" % (
        input_airline_name, airline_id)

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        return redirect('/airlines')

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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 50259))
    app.run(port=port, debug=True)