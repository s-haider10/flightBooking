CREATE TABLE airline(
  name_of_airline varchar(50) NOT NULL,
  PRIMARY KEY (name_of_airline)
) engine=InnoDB default charset=latin1;

CREATE TABLE airline_staff (
  email varchar(50) NOT NULL,
  password varchar(50) NOT NULL,
  first_name varchar(50) NOT NULL,
  last_name varchar(50) NOT NULL,
  date_of_birth varchar(50) NOT NULL,
  operator_permission boolean NOT NULL,
  admin_permission boolean NOT NULL,
  name_of_airline varchar(50) NOT NULL,
  PRIMARY KEY (email),
  FOREIGN KEY (name_of_airline) REFERENCES airline(name_of_airline) ON DELETE CASCADE ON UPDATE CASCADE
) engine=InnoDB default charset=latin1;

-- adding the seats attribute here as instructed by Professor Lihua.
CREATE TABLE airplane(
  name_of_airline varchar(50) NOT NULL,
  ID_airplane int(15) NOT NULL,
  num_of_seats int(5) NOT NULL,
  PRIMARY KEY (ID_airplane),
  FOREIGN KEY (name_of_airline) REFERENCES airline(name_of_airline) ON DELETE CASCADE ON UPDATE CASCADE
) engine=InnoDB default charset=latin1;

CREATE TABLE airport (
  name varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  PRIMARY KEY (name)
) engine=InnoDB default charset=latin1;

CREATE TABLE booking_agent (
  email varchar(50) NOT NULL,
  password varchar(50) NOT NULL,
  booking_agent_ID int(15) NOT NULL,
  PRIMARY KEY (email)
) engine=InnoDB default charset=latin1;

CREATE TABLE customer(
  email varchar(50) NOT NULL,
  name varchar(50) NOT NULL,
  password varchar(50) NOT NULL,
  building_number varchar(50) NOT NULL,
  street_address varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state varchar(50) NOT NULL,
  phone_num int(20) NOT NULL,
  passport_num varchar(40) NOT NULL,
  passport_expiration date NOT NULL,
  passport_country varchar(50) NOT NULL,
  date_of_birth date NOT NULL,
  PRIMARY KEY (email)
) engine=InnoDB default charset = latin1;

CREATE TABLE flight(
  name_of_airline varchar(50) NOT NULL,
  flight_num int(15) NOT NULL,
  departure_airport_name varchar(50) NOT NULL,
  departure_time datetime NOT NULL,
  arrival_airport_name varchar(50) NOT NULL,
  arrival_time datetime NOT NULL,
  price decimal(10, 0) NOT NULL,
  status varchar(50) NOT NULL,
  ID_airplane int(15) NOT NULL,
  PRIMARY KEY (flight_num, ID_airplane, name_of_airline),
  FOREIGN KEY (name_of_airline, ID_airplane) REFERENCES airplane(name_of_airline, ID_airplane),
  FOREIGN KEY (departure_airport_name) REFERENCES airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (arrival_airport_name) REFERENCES airport(name) ON DELETE CASCADE ON UPDATE CASCADE
) engine=InnoDB default charset=latin1;


CREATE TABLE ticket(
  ticket_id int(11) NOT NULL,
  name_of_airline varchar(50) NOT NULL,
  flight_num int(15) NOT NULL,
  PRIMARY KEY (ticket_id),
  FOREIGN KEY (name_of_airline) REFERENCES flight(name_of_airline) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (flight_num) REFERENCES flight(flight_num) ON DELETE CASCADE ON UPDATE CASCADE
) engine=InnoDB default charset=latin1;


CREATE TABLE bookings(
  ticket_id int(11) NOT NULL,
  email_customer varchar(50) NOT NULL,
  booking_agent_id int(11),
  booking_date datetime NOT NULL,
  PRIMARY KEY (ticket_id, email_customer),
  FOREIGN KEY (email_customer) REFERENCES customer(email) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id) ON DELETE CASCADE ON UPDATE CASCADE
) engine=InnoDB default charset=latin1;


CREATE TABLE agent_works_for(
  email varchar(50) NOT NULL,
  name_of_airline varchar(50) NOT NULL,
  PRIMARY KEY (email, name_of_airline),
  FOREIGN KEY (email) REFERENCES booking_agent(email) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (name_of_airline) REFERENCES airline(name_of_airline) ON DELETE CASCADE ON UPDATE CASCADE

) engine=InnoDB default charset=latin1;
