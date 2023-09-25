

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";




CREATE TABLE `airline` (
  `name` varchar(255) NOT NULL,
  PRIMARY KEY(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `airline_staff` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `data_of_birth` date DEFAULT NULL,
  `permission` varchar(255) NOT NULL DEFAULT 'Normal',
  `airline_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY(`username`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




CREATE TABLE `airplane` (
  `id` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `seats` int(11) DEFAULT NULL,
  PRIMARY KEY(`airline_name`, `id`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




CREATE TABLE `airport` (
  `name` varchar(255) NOT NULL,
  `city` varchar(255) DEFAULT NULL,
  PRIMARY KEY(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `booking_agent` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `booking_agent_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `customer` (
  `email` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `building_number` varchar(255) DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `passport_number` varchar(255) DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_country` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





CREATE TABLE `flight` (
  `airline_name` varchar(255) NOT NULL,
  `flight_num` varchar(255) NOT NULL,
  `departure_airport` varchar(255) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_airport` varchar(255) NOT NULL,
  `arrival_date` date NOT NULL,
  `arrival_time` time NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `status` varchar(255) NOT NULL,
  `airplane_id` varchar(255) NOT NULL,
  PRIMARY KEY(`airline_name`, `flight_num`),
  FOREIGN KEY(`airline_name`, `airplane_id`) REFERENCES `airplane`(`airline_name`, `id`),
  FOREIGN KEY(`departure_airport`) REFERENCES `airport`(`name`),
  FOREIGN KEY(`arrival_airport`) REFERENCES `airport`(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





CREATE TABLE `ticket` (
  `ticket_id` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `flight_num` varchar(255) NOT NULL,
  PRIMARY KEY(`ticket_id`),
  FOREIGN KEY(`airline_name`, `flight_num`) REFERENCES `flight`(`airline_name`, `flight_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `purchase` (
  `ticket_id` varchar(255) NOT NULL,
  `customer_email` varchar(255) NOT NULL,
  `booking_agent_email` varchar(255) DEFAULT NULL,
  `purchase_date` date NOT NULL,
  PRIMARY KEY(`ticket_id`, `customer_email`),
  FOREIGN KEY(`ticket_id`) REFERENCES `ticket`(`ticket_id`),
  FOREIGN KEY(`customer_email`) REFERENCES `customer`(`email`),
  FOREIGN KEY (`booking_agent_email`) REFERENCES `booking_agent` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




CREATE TABLE `work_for` (
  `booking_agent_email` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  PRIMARY KEY(`booking_agent_email`,`airline_name`),
  FOREIGN KEY(`booking_agent_email`) REFERENCES `booking_agent`(`email`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





