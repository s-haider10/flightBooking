-- Syed Ali Haider, Henry Zhang 

INSERT INTO airline(name_of_airline) VALUES ('Emirates');

INSERT INTO airline_staff(email, password, first_name, last_name, date_of_birth, name_of_airline, operator_permission, admin_permission) VALUES (
  'ty12@Emirates.com', 'qwertyuiop', 'Syed', 'Ali', '1998-06-15', 'Emirates', 1, 1
)

INSERT INTO airplane(name_of_airline, ID_airplane, num_of_seats) VALUES
  ('Emirates', 1, 200),
  ('Emirates', 2, 300),
  ('Emirates', 3, 400);

INSERT INTO airport(name, city) VALUES
  ('Islamabad International Airport', 'Islamabad'),
  ('JFK', 'New York'),
  ('Heathrow International Airport', 'London'),
  ('Dulles International Airport', 'Washington DC'),
  ('Pudong International Airport', 'Shanghai');

INSERT INTO booking_agent(email, password, booking_agent_id) VALUES
  ('ht2293@nyu.edu', '12345qwerty', 1),
  ('ph2231@nyu.edu', '9870qwerty', 2);

INSERT INTO customer(email, name, password, building_number, street_address, city, state, phone_num, passport_num, passport_expiration, passport_country, date_of_birth) VALUES
  ('Customer@nyu.edu', 'Customer', 'e19d5cd5af0378da05f63f891c7467af', '2', 'Metrotech', 'New York', 'New York', 51234, 'P123456', '2020-10-24', 'USA', '1990-04-01'),
  ('one@nyu.edu', 'One', '098f6bcd4621d373cade4e832627b4f6', '6', 'Metrotech', 'New York', 'New York', 59873, 'P53412', '2021-04-05', 'USA', '1990-04-04'),
  ('two@nyu.edu', 'Two', '098f6bcd4621d373cade4e832627b4f6', '5', 'Metrotech', 'New York', 'New York', 58123, 'P436246', '2027-04-20', 'USA', '1992-04-18');

INSERT INTO flight(name_of_airline, flight_num, departure_airport_name, departure_time, arrival_airport_name, arrival_time, price, status, ID_airplane) VALUES
  ('Emirates', 139, 'Islamabad International Airport', '2020-12-20 23:50:00', 'Dulles International Airport', '2020-12-21 08:50:00', '200', 'Upcoming', 1),
  ('Emirates', 296, 'Heathrow International Airport', '2021-01-01 12:00:00', 'Dulles International Airport', '2021-01-01 14:00:00', '420', 'Upcoming', 1),
  ('Emirates', 307, 'Islamabad International Airport', '2020-12-19 22:00:00', 'Dulles International Airport', '2020-12-20 02:00:00', '600', 'Upcoming', 1),
  ('Emirates', 455, 'JFK', '2020-12-25 05:00:00', 'Pudong International Airport', '2020-12-25 07:00:00', '97', 'Upcoming', 3),
  ('Emirates', 915, 'Heathrow International Airport', '2020-09-01 00:00:00', 'Pudong International Airport', '2020-09-01 04:00:00', '500', 'Delayed', 2);

INSERT INTO ticket(ticket_id, name_of_airline, flight_num) VALUES
  (1, 'Emirates', 139),
  (2, 'Emirates', 307),
  (3, 'Emirates', 915),
  (4, 'Emirates', 915),
  (5, 'Emirates', 915),
  (6, 'Emirates', 455),
  (7, 'Emirates', 455),
  (8, 'Emirates', 307),
  (9, 'Emirates', 455);

INSERT INTO bookings(ticket_id, email_customer, booking_agent_id, booking_date) VALUES
  (1, 'Customer@nyu.edu', NULL, '2020-1-01'),
  (2, 'Customer@nyu.edu', 1, '2020-11-17'),
  (3, 'one@nyu.edu', 2, '2020-10-10'),
  (4, 'two@nyu.edu', 2, '2020-10-11'),
  (5, 'Customer@nyu.edu', 1, '2020-09-12'),
  (6, 'one@nyu.edu', NULL, '2020-08-19'),
  (7, 'two@nyu.edu', NULL, '2020-08-23'),
  (8, 'one@nyu.edu', 1, '2020-11-15'),
  (9, 'Customer@nyu.edu', 1, '2020-06-19');
