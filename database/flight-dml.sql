
-- The `:` character is being used to denote variables that will have data
-- that is fetched via backend code

--
-- Airlines
--

-- CREATE: Create a new airline
INSERT INTO airlines (airline_id, name) VALUES 
(:airline_id, :name);

-- READ: Get attributes to populate airline table
SELECT airline_id, 
       name
FROM airlines;

-- READ: Get airline IDs
SELECT airline_id
FROM airlines;

-- READ: Get airline info to populate dropdowns
SELECT CONCAT(airline_id, ' - ', airline_name)
FROM airlines;

-- READ (SEARCH/FILTER): Get attributes to populate airline table when searching
-- for an airline
SELECT airline_id,
       name
FROM airlines
WHERE UPPER(airline_id) LIKE UPPER(CONCAT('%%', :airline_search_bar_input, '%%'))
   OR UPPER(name) LIKE UPPER(CONCAT('%%', :airline_search_bar_input, '%%'));

-- UPDATE: Update an airline's attributes given an airline ID
UPDATE airlines
SET name = :name_input
WHERE airline_id = :airline_id_from_form;

-- DELETE: Delete an airline
DELETE FROM airlines
WHERE airline_id = :airline_id_selected_from_table;


--
-- Airports
--

-- CREATE: Create a new airport
INSERT INTO airports (airport_id, name, location) VALUES
(:airport_id, :name, :location);

-- READ: Get attributes to populate airport table
SELECT airport_id, 
       name, 
       location
FROM airports;

-- READ: Get airport IDs to populate dropdowns
SELECT airport_id
FROM airports;

-- READ: Get airport info to populate dropdowns
SELECT CONCAT(airport_id, ' - ', airport_name)
FROM airports;

-- UPDATE: Update an airport's attribute given an airport ID
UPDATE airports
SET name = :name_input, 
    location = :location_input
WHERE airport_id = :airline_id_from_form;

-- DELETE: Delete an airport
DELETE FROM airports
WHERE airport_id = :airport_id_selected_from_table;


--
-- Flights
--

-- CREATE: Create a new flight
INSERT INTO flights (plane_id, departure_time, arrival_time, origin_airport_id, destination_airport_id) VALUES
(:plane_id_from_form_dropdown, :departure_time, :arrival_time, :origin_airport_id_from_form_dropdown, :destination_airport_id_from_form_dropdown);

-- READ: Get attributes to populate flight table
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
JOIN airports AS origin ON flights.origin_airport_id = origin.airport_id
JOIN airports AS destination ON flights.destination_airport_id = destination.airport_id;

-- READ: Get plane IDs to populate plane dropdown
SELECT plane_id
FROM planes;

-- UPDATE: Update a flight's attributes given a flight ID
UPDATE flights
SET plane_id = :plane_id_from_form_dropdown,
    departure_time = :departure_time_from_form,
    arrival_time = :arrival_time_from_form,
    origin_airport_id = :origin_airport_id_from_form_dropdown,
    destination_airport_id = :destination_airport_id_from_form_dropdown
WHERE flight_id = :flight_id_from_form;

-- DELETE: Delete a flight
DELETE FROM flights
WHERE flight_id = :flight_id_selected_from_table;


--
-- Planes
--

-- CREATE: Create a new plane
INSERT INTO planes (airline_id, passenger_capacity, manufacturer) VALUES
(:airline_id, :passenger_capacity, :manufacturer);

-- READ: Get attributes to populate plane table
SELECT planes.plane_id, 
       airlines.airline_name, 
       planes.passenger_capacity, 
       planes.manufacturer
FROM planes
LEFT JOIN airlines ON planes.airline_id = airlines.airline_id;

-- READ: Get plane IDs to populate plane ID dropdowns
SELECT plane_id
FROM planes;

-- UPDATE: Update a plane's attribute given a plane ID
UPDATE planes
SET airline_id = :airline_id_from_form,
    passenger_capacity = :passenger_capacity_from_form,
    manufacturer = :manufacturer_from_form
WHERE plane_id = :plane_id_from_form;

-- DELETE: Delete a plane
DELETE FROM planes
WHERE plane_id = :plane_id_selected_from_table;


--
-- Airlines-Airports
--

-- CREATE: Creates a transaction row using FK attributes from Airline and
-- Airport entities. This row is created when a new flight is added. Two rows
-- are created with each new flight, one for the origin airport and one for the
-- destination airport
INSERT INTO airlines_airports (airline_id, airport_id) VALUES
((SELECT airline_id FROM planes WHERE plane_id = :plane_id_from_create_flight_form), 
    :origin_airport_id_from_create_flight_form);

INSERT INTO airlines_airports (airline_id, airport_id) VALUES
((SELECT airline_id FROM planes WHERE plane_id = :plane_id_from_create_flight_form),
    :destination_airport_id_from_create_flight_form);

-- CREATE: Creates a transaction row directly from the UI form. Most inserts
-- would likely be a result of adding a new flight, but the ability to insert a
-- row directly into this table has been added per the project specifications.
INSERT INTO airlines_airports(airline_id, airport_id) VALUES
(:airline_id_from_form, :airport_id_from_form);

-- READ: Get attributes to populate airlines-airports table
SELECT id,
       airlines.airline_name,
       airports.airport_name
FROM airlines_airports
JOIN airlines ON airlines_airports.airline_id = airlines.airline_id
JOIN airports ON airlines_airports.airport_id = airports.airport_id;

-- DELETES are handled by CASCADES in the table creations but
-- are included here for the sake of completeness

-- DELETE: Deletes a transaction row if an airline is deleted on the Airlines
-- page
DELETE FROM airlines_airports
WHERE airline_id = :airline_id_selected_from_airline_table;

-- DELETE: Deletes a transaction row if an airport is deleted on the Airports
-- page
DELETE FROM airlines_airports
WHERE airport_id = :airport_id_selected_from_airport_table;

-- DELETE: Deletes a transaction row if selected from the table
DELETE FROM airlines_airports
WHERE id = :id_selected_from_table;