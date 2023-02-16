INSERT INTO airlines (airline_id, name) VALUES
('AAL', 'American Airlines'),
('DAL', 'Delta Air Lines'),
('JBU', 'JetBlue');

INSERT INTO airports (airport_id, name, location) VALUES
('DFW', 'Dallas Fort Worth International Airport', 'Dallas, TX'),
('LGA', 'LaGuardia Airport', 'New York, NY'),
('LAX', 'Los Angeles International Airport', 'Los Angeles, CA'),
('ATL', 'Hartsfield-Jackson Atlanta International Airport', 'Atlanta, GA'),
('ORD', 'Chicago O''Hare International Airport', 'Chicago, IL');

INSERT INTO planes (airline_id, passenger_capacity, manufacturer) VALUES
('DAL', 350, 'Airbus'),
('DAL', 110, 'Boeing'),
('AAL', 76, 'Embraer'),
('JBU', 140, 'Airbus'),
('AAL', 65, 'Bombardier');

INSERT INTO flights (plane_id, departure_time, arrival_time, origin, destination) VALUES
(1, '2022-01-01 09:00:00', '2022-01-01 11:00:00', 'DFW', 'LGA'),
(1, '2022-05-06 14:22:22', '2022-05-06 19:12:34', 'LAX', 'ATL'),
(2, '2021-12-12 23:15:00', '2021-12-13 00:15:00', 'ATL', 'LGA'),
(4, '2020-06-07 11:11:11', '2020-06-07 12:12:12', 'ORD', 'DFW'),
(5, '2022-09-17 04:05:06', '2022-09-17 06:07:08', 'LGA', 'ORD');

INSERT INTO airlines_has_airports (airline_id, airport_id) VALUES
('DAL', 'DFW'),
('AAL', 'LGA'),
('JBU', 'LGA'),
('AAL', 'ATL'),
('JBU', 'ORD'),
('JBU', 'LAX');