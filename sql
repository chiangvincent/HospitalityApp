CREATE TABLE patientdata (
  drg varchar(250),
  provider_id int,
  name varchar(1000),
  address varchar(1000),
  city varchar(1000),
  state varchar(1000),
  zipcode int,
  ref varchar(1000),
  num_discharge int,
  avg_covered int,
  avg_pay int,
  avg_medicare int);

LOAD DATA LOCAL INFILE
'C:/Users/Vincent Chiang/developments/hospitalityapp/data/patient_data.csv'
INTO TABLE patientdata
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

ALTER TABLE patientdatafilteredtwo
MODIFY COLUMN avg_covered decimal(8, 2);

ALTER TABLE patientdatafiltered
ADD COLUMN drg varchar(100) after new;

INSERT INTO patientdatafiltered (drg)
VALUES drg varchar(100) after new;


ALTER TABLE patientdatafilteredtwo drop provider_id, drop zipcode, drop ref, drop num_discharge, drop avg_pay, drop avg_medicare;

ALTER TABLE patientdatafiltered
ADD COLUMN city varchar(100) after new;

INSERT INTO patientdatafiltered (city)
SELECT b.city from patientdata as b, patientdatafiltered as a;

CREATE TABLE PATIENTDATAFILTEREDTWO AS
SELECT * FROM PATIENTDATA;
