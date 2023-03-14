-- -----------------------------------------------------------------------------
-- CS 340 Portfolio Project
-- Project Name: FAA Database
-- Group Members: Matthew Meyer, Roman Sosiak
-- Group #: 69
-- -----------------------------------------------------------------------------

-- The `:` character is being used to denote variables that will have data
-- that is fetched via backend code


-- -----------------------------------------------------------------------------
-- Airlines Queries
-- -----------------------------------------------------------------------------

-- CREATE: Create a new airline.
INSERT INTO airlines (airline_id, name) VALUES 
(:airline_id, :name_input);

-- READ: Get attributes to populate airline table.
SELECT airline_id, 
       name
FROM airlines
ORDER BY airline_id;

-- READ: Get airline IDs.
SELECT airline_id
FROM airlines;

-- READ: Get airline info to populate dropdowns.
SELECT airline_id,
       CONCAT(airline_id, ' - ', name) as airline_info
FROM airlines;

-- READ (SEARCH/FILTER): Get attributes to populate airline table when using
-- search functionality.
SELECT airline_id,
       name
FROM airlines
WHERE UPPER(airline_id) LIKE UPPER(CONCAT('%%', :airline_search_bar_input, '%%'))
   OR UPPER(name) LIKE UPPER(CONCAT('%%', :airline_search_bar_input, '%%'));

-- READ: Get airline ID. Used to determine if airline ID already exists in DB
-- when requesting to add airline to DB.
SELECT airline_id
FROM airlines
WHERE airline_id = :airline_id_input;

-- UPDATE: Update an airline's attributes given an airline ID.
UPDATE airlines
SET name = :name_input_from_update_form
WHERE airline_id = :airline_id_from_table;

-- DELETE: Delete an airline given an airline ID.
DELETE FROM airlines
WHERE airline_id = :airline_id_from_table;


-- -----------------------------------------------------------------------------
-- Airports queries
-- -----------------------------------------------------------------------------

-- CREATE: Create a new airport.
INSERT INTO airports (airport_id, name, location) VALUES
(:airport_id_input, :name_input, :location_input);

-- READ: Get attributes to populate airport table.
SELECT airport_id, 
       name, 
       location
FROM airports
ORDER BY airport_id;

-- READ: Get airport info to populate dropdowns.
SELECT airport_id
FROM airports;

-- READ: Get airport info to populate dropdowns.
SELECT CONCAT(airport_id, ' - ', airport_name)
FROM airports;

-- READ: Get airport ID. Used to determine if airport ID already exists in DB
-- when requesting to add airport to DB.
SELECT airport_id
FROM airports
WHERE airport_id = :airport_id_input;

-- UPDATE: Update an airport's attribute given an airport ID.
UPDATE airports
SET name = :name_input, 
    location = :location_input
WHERE airport_id = :airline_id_from_table;

-- DELETE: Delete an airport given an airport ID.
DELETE FROM airports
WHERE airport_id = :airport_id_from_table;


-- -----------------------------------------------------------------------------
-- Flights queries
-- -----------------------------------------------------------------------------

-- CREATE: Create a new flight.
INSERT INTO flights (plane_id, departure_time, arrival_time, origin_airport_id, destination_airport_id) VALUES
(:plane_id_input, :departure_time_input, :arrival_time_input, :origin_airport_id_input, :destination_airport_id_input);

-- READ: Get attributes to populate flight table.
SELECT flights.flight_id,
       flights.plane_id,
       planes.manufacturer,
       airlines.name as airline_name,
       flights.departure_time,
       flights.arrival_time,
       origin.name AS origin_airport_name,
       destination.name as destination_airport_name
FROM flights
JOIN planes
    ON flights.plane_id = planes.plane_id
LEFT JOIN airlines
    ON planes.airline_id = airlines.airline_id
JOIN airports AS origin
    ON flights.origin_airport_id = origin.airport_id
JOIN airports AS destination
    ON flights.destination_airport_id = destination.airport_id;

-- READ: Get plane IDs to populate plane dropdown.
SELECT plane_id
FROM planes;

-- UPDATE: Update a flight's attributes given a flight ID
UPDATE flights
SET plane_id = :plane_id_input,
    departure_time = :departure_time_input,
    arrival_time = :arrival_time_input,
    origin_airport_id = :origin_airport_id_input,
    destination_airport_id = :destination_airport_id_input
WHERE flight_id = :flight_id_input;

-- DELETE: Delete a flight.
DELETE FROM flights
WHERE flight_id = :flight_id_from_table;


-- -----------------------------------------------------------------------------
-- Planes queries
-- -----------------------------------------------------------------------------

-- CREATE: Create a new plane.
INSERT INTO planes (airline_id, passenger_capacity, manufacturer) VALUES
(:airline_id, :passenger_capacity, :manufacturer);

-- READ: Get attributes to populate plane table.
SELECT planes.plane_id,
       airlines.airline_id AS airline_id,
       airlines.name AS airline_name, 
       planes.passenger_capacity, 
       planes.manufacturer
FROM planes
LEFT JOIN airlines
    ON planes.airline_id = airlines.airline_id;

-- READ: Get plane info to populate plane dropdowns.
SELECT planes.plane_id,
       REPLACE(CONCAT(planes.plane_id, ' - ',, airlines.name, ' - ',
        planes.manufacturer), ' ', '') AS plane_info       
FROM planes
LEFT JOIN airlines
    ON planes.airline_id = airlines.airline_id;

-- UPDATE: Update a plane's attribute given a plane ID.
UPDATE planes
SET airline_id = :airline_id_input,
    passenger_capacity = :passenger_capacity_input,
    manufacturer = :manufacturer_input
WHERE plane_id = :plane_id_input;

-- DELETE: Delete a plane.
DELETE FROM planes
WHERE plane_id = :plane_id_from_table;


-- -----------------------------------------------------------------------------
-- Airlines-Airports
-- -----------------------------------------------------------------------------

-- CREATE: Creates a transaction row using FK attributes from Airline and
-- Airport entities. This row is created when a new flight is added. Two rows
-- are created with each new flight, one for the origin airport and one for the
-- destination airport.
INSERT INTO airlines_airports (airline_id, airport_id) VALUES
((SELECT airline_id FROM planes WHERE plane_id = :plane_id_input), 
    :origin_airport_id_input);

INSERT INTO airlines_airports (airline_id, airport_id) VALUES
((SELECT airline_id FROM planes WHERE plane_id = :plane_id_input),
    :destination_airport_id_input);

-- CREATE: Creates a transaction row directly from the UI form. Most inserts
-- would likely be a result of adding a new flight, but the ability to insert a
-- row directly into this table has been added per the project specifications.
INSERT INTO airlines_airports(airline_id, airport_id) VALUES
(:airline_id_input, :airport_id_input);

-- READ: Get attributes to populate airlines-airports table.
SELECT airline_airport_idid,
       airlines.airline_name,
       airports.airport_name
FROM airlines_airports
JOIN airlines ON airlines_airports.airline_id = airlines.airline_id
JOIN airports ON airlines_airports.airport_id = airports.airport_id;

-- DELETES are handled by CASCADES in the table creations.
-- Deleting an airline_id or airport_id will remove transactions that have a
-- particular airline_id or airport_id.