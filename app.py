import MySQLdb
from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL
from flask import request
import os

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/airlines', methods=['POST', 'GET'])
def airlines():

    if request.method == 'GET':

        search_query = request.args

        if search_query:
            search_query = search_query['search']
            query = """SELECT airline_id,
                                name
                        FROM airlines
                        WHERE UPPER(airline_id) LIKE UPPER(CONCAT('%%', '%s',
                            '%%'))
                           OR UPPER(name) LIKE UPPER(CONCAT('%%', '%s', '%%'))
                    """ % (search_query, search_query)
        else:
            query = "SELECT airline_id, name FROM airlines ORDER BY airline_id"

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airlines = cur.fetchall()

        return render_template(
            "airlines.j2",
            airlines=db_airlines)

    if request.method == 'POST':
        input_airline_id = request.form['input-airline-id']
        input_airline_name = request.form['input-airline-name']

        input_airline_id = input_airline_id.upper()
        input_airline_id = input_airline_id.replace("'", "''")

        query = """
                SELECT airline_id
                FROM airlines
                WHERE airline_id = '%s'
                """ % (input_airline_id)

        cur = mysql.connection.cursor()
        cur.execute(query)

        existing_airline_id = cur.fetchall()
        airline_id_error = False

        if len(existing_airline_id) > 0:
            airline_id_error = True

        if not input_airline_id.isalpha():
            airline_id_error = True

        query = """
                INSERT INTO airlines (airline_id, name)
                VALUES ('%s', '%s')""" % (input_airline_id, input_airline_name)

        if not airline_id_error:
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect('/airlines')
        else:
            airline_id_error = """
                Airline ID already exists or contains non-alphabet characters.
            """
            query = "SELECT airline_id, name FROM airlines ORDER BY airline_id"
            cur = mysql.connection.cursor()
            cur.execute(query)
            db_airlines = cur.fetchall()

            return render_template('airlines.j2',
                                   airlines=db_airlines,
                                   error=airline_id_error)


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
        query = """
                SELECT airline_id,
                        name
                FROM airlines WHERE airline_id = '%s'
                """ % (airline_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airlines = cur.fetchone()
        cur.close()

        return render_template(
            "forms/update_airlines.j2",
            airlines=db_airlines)

    if request.method == 'POST':
        input_airline_name = request.form['airline-name']

        query = """
                UPDATE airlines
                SET name = '%s'
                WHERE airline_id = '%s'""" % (input_airline_name, airline_id)

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        return redirect('/airlines')


@app.route('/airlines_airports')
def airlines_airports():
    return render_template("airlines_airports.html")


@app.route('/airports', methods=['POST', 'GET'])
def airports():

    if request.method == 'GET':
        query = """
                SELECT airport_id,
                    name,
                    location
                FROM airports
                ORDER BY airport_id
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airports = cur.fetchall()

        return render_template(
            "airports.j2",
            airports=db_airports)

    if request.method == 'POST':

        input_airport_id = request.form['input-airport-id']
        input_airport_name = request.form['input-airport-name']
        input_airport_location = request.form['input-airport-location']

        input_airport_id = input_airport_id.upper()

        input_airport_name = input_airport_name.replace("'", "''")
        input_airport_location = input_airport_location.replace("'", "''")

        query = """
                SELECT airport_id
                FROM airports
                WHERE airport_id = '%s'
                """ % (input_airport_id)

        cur = mysql.connection.cursor()
        cur.execute(query)

        existing_airport_id = cur.fetchall()
        airport_id_error = False

        if len(existing_airport_id) > 0:
            airport_id_error = True

        if not input_airport_id.isalpha():
            airport_id_error = True

        query = """
                INSERT INTO airports (airport_id, name, location) VALUES
                ('%s', '%s', '%s')
                """ % (
            input_airport_id,
            input_airport_name,
            input_airport_location)

        if not airport_id_error:
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect('/airports')
        else:
            airport_id_error = """
                Airport ID already exists or contains non-alphabet characters.
            """

            query = """
                SELECT airport_id,
                    name,
                    location
                FROM airports
                ORDER BY airport_id
                """
            cur = mysql.connection.cursor()
            cur.execute(query)
            db_airports = cur.fetchall()

            return render_template('airports.j2',
                                   airports=db_airports,
                                   error=airport_id_error)


@app.route('/delete_airport/<string:airport_id>')
def delete_airport(airport_id):
    query = "DELETE FROM airports WHERE airport_id = '%s'" % (airport_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return redirect('/airports')


@app.route('/update_airport/<string:airport_id>', methods=['POST', 'GET'])
def update_airport(airport_id):

    if request.method == 'GET':
        query = """
                SELECT airport_id,
                        name,
                        location
                FROM airports
                WHERE airport_id = '%s'
                """ % (airport_id)

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airports = cur.fetchone()
        cur.close()

        return render_template(
            "forms/update_airports.j2",
            airports=db_airports
        )

    if request.method == 'POST':
        input_airport_name = request.form['update-airport-name']
        input_airport_location = request.form['update-airport-location']

        input_airport_name = input_airport_name.replace("'", "''")
        input_airport_location = input_airport_location.replace("'", "''")

        query = """
                UPDATE airports
                SET name = '%s',
                    location = '%s'
                WHERE airport_id = '%s'
                """ % (input_airport_name, input_airport_location, airport_id)

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        return redirect('/airports')


@app.route('/flights')
def flights():
    return render_template("flights.html")


@app.route('/planes', methods=['POST', 'GET'])
def planes():

    if request.method == 'GET':

        query = """
                SELECT planes.plane_id,
                        airlines.airline_id,
                        airlines.name AS airline_name,
                        planes.passenger_capacity,
                        planes.manufacturer
                FROM planes
                LEFT JOIN airlines ON planes.airline_id = airlines.airline_id
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_planes = cur.fetchall()

        query = """
                SELECT airline_id,
                    CONCAT(airline_id, ' - ', name) as airline_info
                FROM airlines
                """

        cur.execute(query)
        db_airlines = cur.fetchall()

        return render_template(
            "planes.j2",
            planes=db_planes,
            airlines=db_airlines)

    if request.method == 'POST':

        input_airline_id = request.form['input-airline-id']
        input_passenger_capacity = request.form['input-passenger-capacity']
        input_manufacturer = request.form['input-manufacturer']

        if input_airline_id == 'null':
            input_airline_id = None

        if input_manufacturer == 'null':
            input_manufacturer = None

        if input_airline_id and input_manufacturer:
            query = """
                    INSERT INTO planes (airline_id, passenger_capacity,
                        manufacturer) VALUES
                    ('%s', '%s', '%s')
                    """ % (
                input_airline_id,
                input_passenger_capacity,
                input_manufacturer)

        if input_airline_id and not input_manufacturer:
            query = """
                    INSERT INTO planes (airline_id, passenger_capacity,
                        manufacturer) VALUES
                    ('%s', '%s', NULL)
                    """ % (input_airline_id, input_passenger_capacity)

        if not input_airline_id and input_manufacturer:
            query = """
                    INSERT INTO planes (airline_id, passenger_capacity,
                        manufacturer) VALUES
                    (NULL, '%s', '%s')
                    """ % (input_passenger_capacity, input_manufacturer)

        if not input_airline_id and not input_manufacturer:
            query = """
                    INSERT INTO planes (airline_id, passenger_capacity,
                        manufacturer) VALUES
                    (NULL, '%s', NULL)
                    """ % (input_passenger_capacity)

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        return redirect('/planes')


@app.route('/update_plane/<int:plane_id>', methods=['POST', 'GET'])
def update_plane(plane_id):

    if request.method == 'GET':
        query = """
                SELECT planes.plane_id,
                        airlines.airline_id AS airline_id,
                        airlines.name AS airline_name,
                        planes.passenger_capacity,
                        planes.manufacturer
                FROM planes
                LEFT JOIN airlines ON planes.airline_id = airlines.airline_id
                WHERE plane_id = '%s'
                """ % (plane_id)

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_planes = cur.fetchone()

        query = """
                SELECT airline_id,
                        CONCAT(airline_id, ' - ', name) AS airline_info
                FROM airlines
                """

        cur.execute(query)
        db_airlines = cur.fetchall()

        cur.close()

        return render_template(
            "forms/update_planes.j2",
            planes=db_planes,
            airlines=db_airlines)

    if request.method == 'POST':
        input_airline_id = request.form['update-airline-id']
        input_passenger_capacity = request.form['update-passenger-capacity']
        input_manufacturer = request.form['update-manufacturer']

        if input_airline_id == 'null' or input_airline_id == 'None' or \
                input_airline_id == '':
            input_airline_id = None

        if input_manufacturer == 'null' or input_manufacturer == 'None' or \
                input_manufacturer == '':
            input_manufacturer = None

        if input_airline_id and input_manufacturer:
            query = """
                    UPDATE planes
                    SET airline_id = '%s',
                        passenger_capacity = '%s',
                        manufacturer = '%s'
                    WHERE plane_id = '%s'
                    """ % (
                input_airline_id,
                input_passenger_capacity,
                input_manufacturer,
                plane_id
                    )

        if input_airline_id and not input_manufacturer:
            query = """
                    UPDATE planes
                    SET airline_id = '%s',
                        passenger_capacity = '%s',
                        manufacturer = NULL
                    WHERE plane_id = '%s'
                    """ % (
                input_airline_id,
                input_passenger_capacity,
                plane_id
                    )

        if not input_airline_id and input_manufacturer:
            query = """
                    UPDATE planes
                    SET airline_id = NULL,
                        passenger_capacity = '%s',
                        manufacturer = '%s'
                    WHERE plane_id = '%s'
                    """ % (
                input_passenger_capacity,
                input_manufacturer,
                plane_id
                    )

        if not input_airline_id and not input_manufacturer:
            query = """
                    UPDATE planes
                    SET airline_id = NULL,
                        passenger_capacity = '%s',
                        manufacturer = NULL
                    WHERE plane_id = '%s'
                    """ % (
                input_passenger_capacity,
                plane_id
                    )

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        return redirect('/planes')


@app.route('/delete_plane/<string:plane_id>')
def delete_plane(plane_id):
    query = "DELETE FROM planes WHERE plane_id = '%s'" % (plane_id)

    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return redirect('/planes')


@app.errorhandler(MySQLdb.Error)
def db_error(error):
    return render_template('error.j2', error=error), 500


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 50259))
    app.run(port=port, debug=True)
