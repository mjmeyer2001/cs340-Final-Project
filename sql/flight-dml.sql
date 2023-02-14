-- TODO:
-- Flights - READ

-- Colon (:) character is being used to denote variables that will have data
-- that is fetched via backend code

--
-- Airlines
--

-- CREATE: Create a new airline
INSERT INTO airlines VALUES 
(:airline_id, :name);

-- READ: Get attributes to populate airline table
SELECT airline_id, 
       name
FROM airlines;

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
INSERT INTO airports VALUES
(:airport_id, :name, :location);

-- READ: Get attributes to populate airport table
SELECT airport_id, 
       name, 
       location
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
INSERT INTO flights VALUES
(:plane_id, :departure_time, :arrival_time, :origin_airport_id, :destination_airport_id);

-- READ: Get attributes to populate flight table

-- UPDATE: Update a flight's attributes given a flight ID
UPDATE flights
SET plane_id = :plane_id_from_form,
    departure_time = :departure_time_from_form,
    arrival_time = :arrival_time_from_form,
    origin_airport_id = :origin_airport_id_from_form,
    destination_airport_id = :destination_airport_id_from_form
WHERE flight_id = :flight_id_from_form;

-- DELETE: Delete a flight
DELETE FROM flights
WHERE flight_id = :flight_id_selected_from_table;


--
-- Planes
--

-- CREATE: Create a new plane
INSERT INTO planes VALUES
(:airline_id, :passenger_capacity, :manufacturer);

-- READ: Get attributes to populate plane table
SELECT planes.plane_id, 
       airlines.airline_name, 
       planes.passenger_capacity, 
       planes.manufacturer
FROM planes
LEFT JOIN airlines ON planes.airline_id = airlines.airline_id;

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

-- READ: Get attributes to populate airlines-airports table
SELECT airlines_airports.airline_airport_id
FROM airlines_airports
JOIN airlines ON airlines_airports.airline_id = airlines.airline_id
JOIN airports ON airlines_airports.airports_id = airports.airport_id;