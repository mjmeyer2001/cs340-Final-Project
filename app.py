# Structure of code (database configuration and routing) adapted from CS340
# Flask starter app code.

# General Flask knowledge taken from official Flask tutorial
# https://flask.palletsprojects.com/en/2.2.x/tutorial/

import MySQLdb
from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL
from flask import request
import os

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# get config variables from .env file
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# Routes

@app.route('/')
def root():
    # render homepage
    return render_template("index.html")


@app.route('/airlines', methods=['POST', 'GET'])
def airlines():

    # read operation to get airlines data from DB
    if request.method == 'GET':

        # The request.args attribute(namely, the 'search' key) is used to check
        # if the user has entered text into the search airline box. If so
        # (request.args is not None), a query is run to only grab data with
        # "matching" airline_id or airline name.
        # https://stackoverflow.com/questions/34671217/in-flask-what-is-request-args-and-how-is-it-used
        search_query = request.args

        if search_query:
            search_query = search_query['search']
            # escape % using two %s to handle issues with Jinja's
            # interpretation of %
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

        # render template with appropriate airlines
        return render_template(
            "airlines.j2",
            airlines=db_airlines)

    # create operation to add new airline to DB
    if request.method == 'POST':
        input_airline_id = request.form['input-airline-id']
        input_airline_name = request.form['input-airline-name']

        input_airline_id = input_airline_id.upper()
        # escaping single quotes
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

        # validating airline ID (should not be empty string and should only
        # contain alphabet characters)
        if len(existing_airline_id) > 0:
            airline_id_error = True

        if not input_airline_id.isalpha():
            airline_id_error = True

        query = """
                INSERT INTO airlines (airline_id, name)
                VALUES ('%s', '%s')""" % (input_airline_id, input_airline_name)

        # if no errors present, insert data into DB and redirect to airlines
        # page
        if not airline_id_error:
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect('/airlines')
        else:
            # insert operation does not occur due to error
            airline_id_error = """
                Airline ID already exists or contains non-alphabet characters.
            """
            query = "SELECT airline_id, name FROM airlines ORDER BY airline_id"
            cur = mysql.connection.cursor()
            cur.execute(query)
            db_airlines = cur.fetchall()

            # rendering airlines page with error message on page
            return render_template('airlines.j2',
                                   airlines=db_airlines,
                                   error=airline_id_error)


@app.route('/delete_airline/<string:airline_id>')
def delete_airline(airline_id):
    # delete operation based on selected airline ID
    query = "DELETE FROM airlines WHERE airline_id = '%s'" % (airline_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return redirect('/airlines')


@app.route('/update_airline/<string:airline_id>', methods=['POST', 'GET'])
def update_airline(airline_id):
    # read operation to get info for specific airline to be updated
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

        # render update airline form with data fetched with GET request
        return render_template(
            "forms/update_airlines.j2",
            airlines=db_airlines)

    # update operation
    if request.method == 'POST':
        # grab airline name from form
        input_airline_name = request.form['airline-name']

        # runs update query using selected airline ID and new airline name
        # from update form
        query = """
                UPDATE airlines
                SET name = '%s'
                WHERE airline_id = '%s'
                """ % (input_airline_name, airline_id)

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        return redirect('/airlines')


@app.route('/airlines_airports', methods=['POST', 'GET'])
def airlines_airports():
    # read operation to get airlines-airports data to populate frontend table
    if request.method == 'GET':
        query = """
                SELECT airline_airport_id,
                        airlines.name AS airline_name,
                        airports.name AS airport_name
                FROM airlines_airports
                JOIN airlines
                    ON airlines_airports.airline_id = airlines.airline_id
                JOIN airports
                    ON airlines_airports.airport_id = airports.airport_id
                ORDER BY airline_airport_id
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_transactions = cur.fetchall()

        # read operation to get airport info to populate dropdown in create
        # form
        query = """
                SELECT airport_id,
                    CONCAT(airport_id, ' - ', name) as airport_info
                FROM airports
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airports = cur.fetchall()

        # read operation to get airport info to populate dropdown in create
        # form
        query = """
                SELECT airline_id,
                    CONCAT(airline_id, ' - ', name) as airline_info
                FROM airlines
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airlines = cur.fetchall()

        # render airlines-airport page with all transactions, and dropdowns
        # populated with airlines and airports from DB
        return render_template(
            "airlines_airports.j2",
            transactions=db_transactions,
            airlines=db_airlines,
            airports=db_airports)

    if request.method == 'POST':
        # create operation to add to DB
        # user input from form
        input_airline_id = request.form['input-airline-id-transaction']
        input_airport_id = request.form['input-airport-id-transaction']

        # SQL query to insert
        query = """
                INSERT INTO airlines_airports (airline_id, airport_id) VALUES
                ('%s', '%s')
                """ % (
                input_airline_id,
                input_airport_id
                )

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        return redirect("/airlines_airports")


@app.route('/airports', methods=['POST', 'GET'])
def airports():
    # read operation to populate airports table
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

        # renders template with airports fetched from GET request
        return render_template(
            "airports.j2",
            airports=db_airports)

    if request.method == 'POST':
        # create operation to add new airport to DB
        # gets user input from form
        input_airport_id = request.form['input-airport-id']
        input_airport_name = request.form['input-airport-name']
        input_airport_location = request.form['input-airport-location']

        input_airport_id = input_airport_id.upper()

        input_airport_name = input_airport_name.replace("'", "''")
        input_airport_location = input_airport_location.replace("'", "''")

        # SQL query to check for duplicate airport ID
        query = """
                SELECT airport_id
                FROM airports
                WHERE airport_id = '%s'
                """ % (input_airport_id)

        cur = mysql.connection.cursor()
        cur.execute(query)

        existing_airport_id = cur.fetchall()
        airport_id_error = False

        # server-side validation of airport ID (should not be empty string, and
        # should only be alphabet characters)
        if len(existing_airport_id) > 0:
            airport_id_error = True

        if not input_airport_id.isalpha():
            airport_id_error = True

        # generating SQL query to insert data into DB
        query = """
                INSERT INTO airports (airport_id, name, location) VALUES
                ('%s', '%s', '%s')
                """ % (
            input_airport_id,
            input_airport_name,
            input_airport_location)

        if not airport_id_error:
            # if no error, we execute the SQL query and redirect to airports
            # page
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

            # render the airports page without executing the insert statement
            # renders the page with error message present in the create form
            return render_template('airports.j2',
                                   airports=db_airports,
                                   error=airport_id_error)


@app.route('/delete_airport/<string:airport_id>')
def delete_airport(airport_id):
    # delete operation based on airport ID
    query = "DELETE FROM airports WHERE airport_id = '%s'" % (airport_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return redirect('/airports')


@app.route('/update_airport/<string:airport_id>', methods=['POST', 'GET'])
def update_airport(airport_id):
    # read operation to fetch airport info based on airport ID
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

        # renders the update airports form, displaying data from SQL query
        # executed above
        return render_template(
            "forms/update_airports.j2",
            airports=db_airports
        )

    if request.method == 'POST':
        # update operation
        # get user input from update form
        input_airport_name = request.form['update-airport-name']
        input_airport_location = request.form['update-airport-location']

        # escaping single quotes
        input_airport_name = input_airport_name.replace("'", "''")
        input_airport_location = input_airport_location.replace("'", "''")

        # executing SQL query to update airport info
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


@app.route('/flights', methods=['POST', 'GET'])
def flights():
    # read operation to populate flights data
    if request.method == 'GET':
        query = """
                SELECT flights.flight_id,
                        flights.plane_id,
                        planes.manufacturer,
                        airlines.name as airline_name,
                        flights.departure_time,
                        flights.arrival_time,
                        origin.name AS origin_airport_name,
                        destination.name as destination_airport_name
                FROM flights
                JOIN planes ON flights.plane_id = planes.plane_id
                LEFT JOIN airlines ON planes.airline_id = airlines.airline_id
                JOIN airports AS origin
                    ON flights.origin_airport_id = origin.airport_id
                JOIN airports AS destination
                    ON flights.destination_airport_id = destination.airport_id
                ORDER BY flights.flight_id
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_flights = cur.fetchall()

        # read operation to get plane data to populate plane dropdown menu
        query = """
                SELECT planes.plane_id,
                        REPLACE(CONCAT(planes.plane_id, ' - ',
                        COALESCE(airlines.name, 'NO AIRLINE'), ' - ',
                        COALESCE(planes.manufacturer, 'NO MANUFACTURER')),
                        ' ', ' ') AS plane_info
                FROM planes
                LEFT JOIN airlines ON planes.airline_id = airlines.airline_id
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_planes = cur.fetchall()

        # read operation to get airport data to populate origin airport and
        # destination airport dropdown menus
        query = """
                SELECT airport_id,
                    CONCAT(airport_id, ' - ', name) as airport_info
                FROM airports
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airports = cur.fetchall()

        # renders flights page with appropriate flights, planes, airports
        return render_template(
                "flights.j2",
                flights=db_flights,
                planes=db_planes,
                airports=db_airports)

    if request.method == 'POST':
        # create operation to insert new flight into DB
        # get user input from form
        input_plane_id = request.form['input-plane-id']
        input_departure_time = request.form['input-departure-time']
        input_arrival_time = request.form['input-arrival-time']
        input_origin_airport = request.form['input-origin-airport-id']
        input_destination_airport = request.form[
            'input-destination-airport-id']

        if input_arrival_time == 'null':
            input_arrival_time = None

        if input_departure_time == 'null':
            input_departure_time = None

        # non-null departure time and arrival time
        if input_departure_time and input_arrival_time:
            query = """
                    INSERT INTO flights (plane_id, departure_time,
                        arrival_time,
                    origin_airport_id, destination_airport_id) VALUES
                    ('%s', '%s', '%s', '%s', '%s')
                    """ % (
                input_plane_id,
                input_departure_time,
                input_arrival_time,
                input_origin_airport,
                input_destination_airport
                )

        # non-null departure time, null arrival time
        if input_departure_time and not input_arrival_time:
            query = """
                    INSERT INTO flights (plane_id, departure_time,
                    origin_airport_id, destination_airport_id) VALUES
                    ('%s', '%s', '%s', '%s')
                    """ % (
                input_plane_id,
                input_departure_time,
                input_origin_airport,
                input_destination_airport
                )

        # null departure time, null arrival time
        if not input_departure_time and input_arrival_time:
            query = """
                    INSERT INTO flights (plane_id, arrival_time,
                    origin_airport_id, destination_airport_id) VALUES
                    ('%s', '%s', '%s', '%s')
                    """ % (
                input_plane_id,
                input_arrival_time,
                input_origin_airport,
                input_destination_airport
                )

        # null departure time and null arrival time
        if not input_departure_time and not input_arrival_time:
            query = """
                    INSERT INTO flights (plane_id,
                    origin_airport_id, destination_airport_id) VALUES
                    ('%s', '%s', '%s')
                    """ % (
                input_plane_id,
                input_origin_airport,
                input_destination_airport
                     )

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        # read operation to get airline ID for a particular plane
        query = """
                SELECT airline_id FROM planes
                WHERE plane_id = '%s'
                """ % (input_plane_id)

        cur = mysql.connection.cursor()
        cur.execute(query)
        result = cur.fetchone()
        airline_id = result['airline_id']

        # insert operation to populate M:M airlines_airports table with
        # airline ID, origin airport ID
        if airline_id:
            query = """
                    INSERT INTO airlines_airports
                    (airline_id, airport_id) VALUES
                    ('%s', '%s')
                    """ % (
                    airline_id,
                    input_origin_airport)

            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()

            cur.close()

        # insert operation to populate M:M airlines_airports table with
        # airline ID, destination airport ID
        if airline_id:
            query = """
                    INSERT INTO airlines_airports
                    (airline_id, airport_id) VALUES
                    ('%s', '%s')
                    """ % (
                    airline_id,
                    input_destination_airport)

            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()

            cur.close()

        return redirect('/flights')


@app.route('/update_flight/<string:flight_id>', methods=['POST', 'GET'])
def update_flight(flight_id):
    # read operation to get flight data for the specific flight ID to populate
    # update form
    if request.method == 'GET':
        query = """
        SELECT flights.flight_id,
                flights.plane_id,
                planes.manufacturer,
                airlines.name as airline_name,
                flights.departure_time,
                flights.arrival_time,
                origin.airport_id AS origin_airport_id,
                origin.name AS origin_airport_name,
                destination.airport_id AS destination_airport_id,
                destination.name AS destination_airport_name
        FROM flights
        JOIN planes ON flights.plane_id = planes.plane_id
        LEFT JOIN airlines ON planes.airline_id = airlines.airline_id
        JOIN airports AS origin
            ON flights.origin_airport_id = origin.airport_id
        JOIN airports AS destination
            ON flights.destination_airport_id = destination.airport_id
        WHERE flights.flight_id = '%s'
        """ % (flight_id)

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_flights = cur.fetchone()

        # read operation to get plane info to populate plane info dropdown on
        # update form
        query = """
                SELECT planes.plane_id,
                        REPLACE(CONCAT(planes.plane_id, ' - ',
                        COALESCE(airlines.name, 'NO AIRLINE'), ' - ',
                        COALESCE(planes.manufacturer, 'NO MANUFACTURER')),
                        ' ', ' ') AS plane_info
                FROM planes
                LEFT JOIN airlines ON planes.airline_id = airlines.airline_id
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_planes = cur.fetchall()

        # read operation to get airport info to populate airport info dropdowns
        # on update form
        query = """
                SELECT airport_id,
                    CONCAT(airport_id, ' - ', name) AS airport_info
                FROM airports
                """

        cur = mysql.connection.cursor()
        cur.execute(query)
        db_airports = cur.fetchall()

        # render update flights page with appropriate flight, planes, airports
        return render_template(
            "forms/update_flights.j2",
            flight=db_flights,
            planes=db_planes,
            airports=db_airports)

    if request.method == 'POST':
        # update operation for flight
        # user inputs from form
        input_plane_id = request.form['update-plane-id']
        input_departure_time = request.form['update-departure-time']
        input_arrival_time = request.form['update-arrival-time']
        input_origin_airport = request.form['update-origin-airport-id']
        input_destination_airport = request.form[
            'update-destination-airport-id']

        if input_arrival_time == 'null':
            input_arrival_time = None

        if input_departure_time == 'null':
            input_departure_time = None

        # non-null departure time and non-null arrival time
        if input_departure_time and input_arrival_time:
            query = """UPDATE flights
                    SET plane_id = '%s',
                    departure_time = '%s',
                    arrival_time = '%s',
                    origin_airport_id = '%s',
                    destination_airport_id = '%s'
                    WHERE flight_id = '%s'
                    """ % (
                        input_plane_id,
                        input_departure_time,
                        input_arrival_time,
                        input_origin_airport,
                        input_destination_airport,
                        flight_id
                    )

        # non-null departure time and null arrival time
        if input_departure_time and not input_arrival_time:
            query = """UPDATE flights
                    SET plane_id = '%s',
                    departure_time = '%s',
                    arrival_time = NULL,
                    origin_airport_id = '%s',
                    destination_airport_id = '%s'
                    WHERE flight_id = '%s'
                    """ % (
                        input_plane_id,
                        input_departure_time,
                        input_origin_airport,
                        input_destination_airport,
                        flight_id
                    )
        # null departure time and non-null arrival time
        if not input_departure_time and input_arrival_time:
            query = """UPDATE flights
                    SET plane_id = '%s',
                    departure_time = NULL,
                    arrival_time = '%s',
                    origin_airport_id = '%s',
                    destination_airport_id = '%s'
                    WHERE flight_id = '%s'
                    """ % (
                        input_plane_id,
                        input_arrival_time,
                        input_origin_airport,
                        input_destination_airport,
                        flight_id
                    )

        # null departure time and null arrival time
        if not input_departure_time and not input_arrival_time:
            query = """UPDATE flights
                    SET plane_id = '%s',
                    departure_time = NULL,
                    arrival_time = NULL,
                    origin_airport_id = '%s',
                    destination_airport_id = '%s'
                    WHERE flight_id = '%s'
                    """ % (
                        input_plane_id,
                        input_origin_airport,
                        input_destination_airport,
                        flight_id
                    )

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        cur.close()

        return redirect('/flights')


@app.route('/delete_flight/<string:flight_id>')
def delete_flight(flight_id):
    # delete operation to delete from flights table based on flight ID
    query = "DELETE FROM flights WHERE flight_id = '%s'" % (flight_id)

    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return redirect('/flights')


@app.route('/planes', methods=['POST', 'GET'])
def planes():
    # read operation to populate planes page with planes from DB
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

        # read operation to fetch airline info to populate dropdown menu
        query = """
                SELECT airline_id,
                    CONCAT(airline_id, ' - ', name) as airline_info
                FROM airlines
                """

        cur.execute(query)
        db_airlines = cur.fetchall()

        # renders planes page with planes and airlines present in DB
        return render_template(
            "planes.j2",
            planes=db_planes,
            airlines=db_airlines)

    if request.method == 'POST':
        # create operation to insert new plane into DB
        # user input from form
        input_airline_id = request.form['input-airline-id']
        input_passenger_capacity = request.form['input-passenger-capacity']
        input_manufacturer = request.form['input-manufacturer']

        if input_airline_id == 'null':
            input_airline_id = None

        if input_manufacturer == 'null':
            input_manufacturer = None

        # non-null airline ID and non-null manufacturer
        if input_airline_id and input_manufacturer:
            query = """
                    INSERT INTO planes (airline_id, passenger_capacity,
                        manufacturer) VALUES
                    ('%s', '%s', '%s')
                    """ % (
                input_airline_id,
                input_passenger_capacity,
                input_manufacturer)

        # non-null airline ID and null manufacturer
        if input_airline_id and not input_manufacturer:
            query = """
                    INSERT INTO planes (airline_id, passenger_capacity,
                        manufacturer) VALUES
                    ('%s', '%s', NULL)
                    """ % (input_airline_id, input_passenger_capacity)

        # null airline ID and non-null manufacturer
        if not input_airline_id and input_manufacturer:
            query = """
                    INSERT INTO planes (airline_id, passenger_capacity,
                        manufacturer) VALUES
                    (NULL, '%s', '%s')
                    """ % (input_passenger_capacity, input_manufacturer)

        # null airline ID and null manufacturer
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

    # read operation to populate update plane page with plane selected from
    # plane page
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

        # read operation to get airline info to populate airline dropdown menus
        query = """
                SELECT airline_id,
                        CONCAT(airline_id, ' - ', name) AS airline_info
                FROM airlines
                """

        cur.execute(query)
        db_airlines = cur.fetchall()

        cur.close()

        # renders update planes page with selected plane and airlines present
        # in DB
        return render_template(
            "forms/update_planes.j2",
            planes=db_planes,
            airlines=db_airlines)

    if request.method == 'POST':
        # user input from update form
        input_airline_id = request.form['update-airline-id']
        input_passenger_capacity = request.form['update-passenger-capacity']
        input_manufacturer = request.form['update-manufacturer']

        if input_airline_id == 'null' or input_airline_id == 'None' or \
                input_airline_id == '':
            input_airline_id = None

        if input_manufacturer == 'null' or input_manufacturer == 'None' or \
                input_manufacturer == '':
            input_manufacturer = None

        # non-null airline ID and non-null manufacturer
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

        # non-null airline ID and null manufacturer
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

        # null airline ID and non-null manufacturer
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

        # null airline ID and null manufacturer
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
    # delete operation to remove plane from DB based on plane ID
    query = "DELETE FROM planes WHERE plane_id = '%s'" % (plane_id)

    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return redirect('/planes')


@app.errorhandler(MySQLdb.Error)
def db_error(error):
    # renders error page for all non-handled errors
    return render_template('error.j2', error=error), 500


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 50260))
    app.run(port=port, debug=True)
