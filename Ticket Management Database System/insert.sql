INSERT INTO `airline` (`name`) VALUES
('China Eastern');

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `data_of_birth`, `permission`, `airline_name`) VALUES
('gus', '81dc9bdb52d04dc20036dbd8313ed055', 'Andrew', 'Green', '1990-09-18', 'Both', 'China Eastern'),
('jack', '81dc9bdb52d04dc20036dbd8313ed055', 'Mary', 'Bird', '1995-09-08', 'Normal', 'China Eastern'),
('toco', 'e2df683bedc3acc8f53bf8b343c0a93f', 'Matt', 'Lee', '1991-03-13', 'Operator', 'China Eastern'),
('qw940@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'Mathieu', 'L', '1998-07-16', 'Both', 'China Eastern');


INSERT INTO `airplane` (`id`, `airline_name`, `seats`) VALUES
('jk123', 'China Eastern', 60),
('jl550', 'China Eastern', 30),
('jojo001', 'China Eastern', 300);

INSERT INTO `airport` (`name`, `city`) VALUES
('CZX', 'Changzhou'),
('FRA', 'Frankfurt'),
('JFK', 'New York City'),
('PKX', 'Bejing'),
('PVG', 'Shanghai');

INSERT INTO `booking_agent` (`email`, `password`, `booking_agent_id`) VALUES
('mike@ehrmantraut.com', '81dc9bdb52d04dc20036dbd8313ed055', '112'),
('jessy@pinkman.com', '81dc9bdb52d04dc20036dbd8313ed055', '112'),
('water@white.com', '81dc9bdb52d04dc20036dbd8313ed055', '155');


INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES 
('bager@bb.com', 'Badder', '81dc9bdb52d04dc20036dbd8313ed055', '1555', 'Century Avenue', 'Shanghai', 'China', '81dc9bdb52d04dc20036dbd8313ed055', 'DB123456', '2023-12-31', 'China', '1994-06-10'),
('kim@wexler.com', 'Claire', '81dc9bdb52d04dc20036dbd8313ed055', '1555', 'Century Avenue', 'Shanghai', 'China', '20001111', 'EA234567', '2027-05-20', 'China', '2000-11-23');

INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_date`, `departure_time`, `arrival_airport`, `arrival_date`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('China Eastern', '1', 'FRA', '2023-12-01', '16:00:00', 'JFK', '2023-12-02', '01:00:00', '2300', 'delayed', 'jk123'),
('China Eastern', '2', 'JFK', '2023-12-02', '16:00:00', 'PVG', '2023-12-03', '01:00:00', '2400', 'in-progress', 'jl550'),
('China Eastern', '3', 'PVG', '2023-12-03', '16:00:00', 'FRA', '2023-12-04', '01:00:00', '2500', 'upcoming', 'jk123'),
('China Eastern', '4', 'JFK', '2023-12-11', '21:24:00', 'PVG', '2023-12-12', '21:25:00', '1000', 'In Progress', 'jk123'),
('China Eastern', '7', 'CZX', '2023-12-10', '02:02:00', 'JFK', '2023-12-11', '03:03:00', '3500', 'upcoming', 'jk123');


INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
('111', 'China Eastern', '1'),
('123', 'China Eastern', '1'),
('335', 'China Eastern', '1'),
('336', 'China Eastern', '1'),
('339', 'China Eastern', '1'),
('222', 'China Eastern', '2'),
('334', 'China Eastern', '2'),
('337', 'China Eastern', '2'),
('333', 'China Eastern', '3'),
('338', 'China Eastern', '3'),
('340', 'China Eastern', '3');


INSERT INTO `purchase` (`ticket_id`, `customer_email`, `booking_agent_email`, `purchase_date`) VALUES
('111', 'bager@bb.com', NULL, '2023-12-01'),
('333', 'kim@wexler.com', 'jessy@pinkman.com', '2023-12-01'),
('334', 'kim@wexler.com', NULL, '2023-12-06'),
('335', 'kim@wexler.com', 'water@white.com', '2023-12-06'),
('336', 'bager@bb.com', 'mike@ehrmantraut.com', '2023-12-08'),
('337', 'bager@bb.com', 'mike@ehrmantraut.com', '2023-12-08'),
('338', 'bager@bb.com', NULL, '2023-12-08'),
('339', 'bager@bb.com', 'water@white.com', '2023-12-08'),
('340', 'bager@bb.com', 'water@white.com', '2023-12-08');


INSERT INTO `work_for` (`booking_agent_email`, `airline_name`) VALUES
('jessy@pinkman.com', 'China Eastern'),
('water@white.com', 'China Eastern'),
('mike@ehrmantraut.com', 'China Eastern');