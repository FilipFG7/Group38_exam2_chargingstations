-- MySQL code that creates a table for storing information
-- about charging stations, users and their consumption 

-- DDL part
-- creates a database
DROP DATABASE IF EXISTS exam2;
CREATE DATABASE exam2;

-- selecting which database to use
USE exam2;

-- creating tables for the database and setting their relations
CREATE TABLE EV_Owner
(
OwnerID int auto_increment not null,
FirstName varchar(50),
LastName varchar(50),
PRIMARY KEY (OwnerID)
);

Create Table car
(
CarID int auto_increment not null,
Model varchar(50),
OwnerID int,
PRIMARY KEY (CarID),
CONSTRAINT car_fk_EV_Owner
FOREIGN KEY (OwnerID) REFERENCES EV_Owner(OwnerID)
);

CREATE TABLE charging_stations
(
StationID varchar(50),
Capacity varchar(50),
Operator varchar(50),
longitude varchar(50),
latitude varchar(50),
PRIMARY KEY (StationID)
);

CREATE TABLE charging_status
(
Personal_Consumption int,
OwnerID int,
CarID int,
Remaining_time int,
StationID varchar(50),
CONSTRAINT charging_status_fk_car
FOREIGN KEY (CarID) REFERENCES car(CarID),
CONSTRAINT charging_status_fk_charging_stations
FOREIGN KEY (StationID) REFERENCES charging_stations(StationID),
CONSTRAINT charging_status_fk_EV_Owner
FOREIGN KEY (OwnerID) REFERENCES EV_Owner(OwnerID)
);


-- DML part
-- Before running this part of the code, please use 
-- table data import wizard by rightclicking the selected database
-- in the schema window(MySQL workbench). Then procceed to import the csv file 
-- included with this code into charging_stations table

-- inserting information into tables
-- can be done using the python part of the program
-- we decide to insert some of the users so that we can test 
-- the functionality of the python code
insert into EV_Owner
VALUES
('1', 'Filip', 'Gavalier'),
('2', 'Roman', 'Chaloupka');

insert into car
values
('1', 'Tesla X', '1'),
('2', 'BMW i3', '2');

insert into charging_status
values
('360', '1', '1', '0', 'node/2923093163'),
('120', '2', '2', '0', 'node/2783998965');
