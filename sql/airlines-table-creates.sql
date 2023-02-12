SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS airlines;

CREATE OR REPLACE TABLE airlines (
    airline_id varchar(3) UNIQUE NOT NULL,
    name varchar(255),
    PRIMARY KEY (airline_id)
);

DROP TABLE IF EXISTS airports;

CREATE OR REPLACE TABLE airports (
	airport_id varchar(3) UNIQUE NOT NULL,
    name varchar(255),
    location varchar(255),
    PRIMARY KEY (airport_id)
);

DROP TABLE IF EXISTS planes;

CREATE OR REPLACE TABLE planes (
	plane_id int AUTO_INCREMENT UNIQUE NOT NULL,
	airline_id varchar(3),
    passenger_capacity int NOT NULL,
    manufacturer varchar(255),
    PRIMARY KEY (plane_id),
    FOREIGN KEY (airline_id) REFERENCES airlines(airline_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS flights;

CREATE OR REPLACE TABLE flights (
	flight_id int AUTO_INCREMENT UNIQUE NOT NULL,
	plane_id int NOT NULL,
    	# may not need airline_id (a plane can only belong to one airline, so is redundant)
    	# airline_id varchar(3) NOT NULL,
    	departure_time datetime,
    	arrival_time datetime,
    	origin varchar(255) NOT NULL,
    	destination varchar(255) NOT NULL,
    	PRIMARY KEY (flight_id),
    	FOREIGN KEY (plane_id) REFERENCES planes(plane_id) ON DELETE CASCADE,
    	#FOREIGN KEY (airline_id) REFERENCES airlines(airline_id) ON DELETE CASCADE,
    	FOREIGN KEY (origin) REFERENCES airports(airport_id) ON DELETE CASCADE,
    	FOREIGN KEY (destination) REFERENCES airports(airport_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS airlines_has_airports;

CREATE OR REPLACE TABLE airlines_has_airports (
    airline_id varchar(3) NOT NULL,
    airport_id varchar(3) NOT NULL,
    FOREIGN KEY (airline_id) REFERENCES airlines(airline_id) ON DELETE CASCADE,
    FOREIGN KEY (airport_id) REFERENCES airports(airport_id) ON DELETE CASCADE
);

/*
SET FOREIGN_KEY_CHECKS = 1;
SET AUTOCOMMIT = 1;
*/
