CREATE DATABASE `source`;
USE `source`;

CREATE TABLE `account` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(20) NOT NULL,
  `last_name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `address` (
  `user_id` INT(10),
  `address` VARCHAR(20),
  `tel` VARCHAR(20),
  INDEX i_user_id (`user_id`),
  FOREIGN KEY f_user_id (`user_id`) REFERENCES `account` (`id`)
);

-- ------------------------

CREATE DATABASE `target`;
USE `target`;

CREATE TABLE `account` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(20) NOT NULL,
  `last_name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `address` (
  `user_id` INT(10),
  `address` VARCHAR(20),
  `tel` VARCHAR(15),
  INDEX i_user_id (`user_id`),
  FOREIGN KEY f_user_id (`user_id`) REFERENCES `account` (`id`)
);
