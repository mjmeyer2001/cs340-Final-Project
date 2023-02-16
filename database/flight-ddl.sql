SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

--
-- Table structure for table `airlines`
--

DROP TABLE IF EXISTS airlines;

CREATE OR REPLACE TABLE airlines (
    airline_id varchar(3) UNIQUE NOT NULL,
    name varchar(75),
    PRIMARY KEY (airline_id)
);

--
-- Table structure for table `airports`
--

DROP TABLE IF EXISTS airports;

CREATE OR REPLACE TABLE airports (
    airport_id varchar(3) UNIQUE NOT NULL,
    name varchar(75),
    location varchar(75),
    PRIMARY KEY (airport_id)
);

--
-- Table structure for table `planes`
--

DROP TABLE IF EXISTS planes;

CREATE OR REPLACE TABLE planes (
    plane_id int AUTO_INCREMENT UNIQUE NOT NULL,
    airline_id varchar(3),
    passenger_capacity int NOT NULL,
    manufacturer varchar(75),
    PRIMARY KEY (plane_id),
    FOREIGN KEY (airline_id) REFERENCES airlines(airline_id) ON DELETE CASCADE
);

--
-- Table structure for table `flights`
--

DROP TABLE IF EXISTS flights;

CREATE OR REPLACE TABLE flights (
    flight_id int AUTO_INCREMENT UNIQUE NOT NULL,
    plane_id int NOT NULL,
    departure_time datetime,
    arrival_time datetime,
    origin_airport_id varchar(75) NOT NULL,
    destination_airport_id varchar(75) NOT NULL,
    PRIMARY KEY (flight_id),
    FOREIGN KEY (plane_id) REFERENCES planes(plane_id) ON DELETE CASCADE,
    FOREIGN KEY (origin_airport_id) REFERENCES airports(airport_id) ON DELETE CASCADE,
    FOREIGN KEY (destination_airport_id) REFERENCES airports(airport_id) ON DELETE CASCADE
);

--
-- Table structure for table `airlines_airports`
--

DROP TABLE IF EXISTS airlines_airports;

CREATE OR REPLACE TABLE airlines_airports (
    airline_airport_id int AUTO_INCREMENT UNIQUE NOT NULL,
    airline_id varchar(3) NOT NULL,
    airport_id varchar(3) NOT NULL,
    PRIMARY KEY (airline_airport_id),
    FOREIGN KEY (airline_id) REFERENCES airlines(airline_id) ON DELETE CASCADE,
    FOREIGN KEY (airport_id) REFERENCES airports(airport_id) ON DELETE CASCADE
);


--
-- Inserting data into table `airlines`
--

INSERT INTO airlines (airline_id, name) VALUES
('AAL', 'American Airlines'),
('DAL', 'Delta Air Lines'),
('JBU', 'JetBlue');

--
-- Inserting data into table `airports`
--

INSERT INTO airports (airport_id, name, location) VALUES
('DFW', 'Dallas Fort Worth International Airport', 'Dallas, TX'),
('LGA', 'LaGuardia Airport', 'New York, NY'),
('LAX', 'Los Angeles International Airport', 'Los Angeles, CA'),
('ATL', 'Hartsfield-Jackson Atlanta International Airport', 'Atlanta, GA'),
('ORD', 'Chicago O''Hare International Airport', 'Chicago, IL');

--
-- Inserting data into table `planes`
--

INSERT INTO planes (airline_id, passenger_capacity, manufacturer) VALUES
('DAL', 350, 'Airbus'),
('DAL', 110, 'Boeing'),
('AAL', 76, 'Embraer'),
('JBU', 140, 'Airbus'),
('AAL', 65, 'Bombardier');

--
-- Inserting data into table `flights`
--

INSERT INTO flights (plane_id, departure_time, arrival_time, origin_airport_id, destination_airport_id) VALUES
(1, '2022-01-01 09:00:00', '2022-01-01 11:00:00', 'DFW', 'LGA'),
(1, '2022-05-06 14:22:22', '2022-05-06 19:12:34', 'LAX', 'ATL'),
(2, '2021-12-12 23:15:00', '2021-12-13 00:15:00', 'ATL', 'LGA'),
(4, '2020-06-07 11:11:11', '2020-06-07 12:12:12', 'ORD', 'DFW'),
(5, '2022-09-17 04:05:06', '2022-09-17 06:07:08', 'LGA', 'ORD');

--
-- Inserting data into table `airlines_airports`
--

INSERT INTO airlines_airports (airline_id, airport_id) VALUES
('DAL', 'DFW'),
('AAL', 'LGA'),
('JBU', 'LGA'),
('AAL', 'ATL'),
('JBU', 'ORD'),
('JBU', 'LAX');

SET FOREIGN_KEY_CHECKS = 1;
SET AUTOCOMMIT = 1;