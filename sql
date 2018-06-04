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

ALTER TABLE patientdatafiltered
MODIFY COLUMN avg_covered decimal(8, 2); 


 alter table patientdatafiltered drop drg, drop provider_id, drop city, drop zipcode, drop ref, drop num_discharge, drop avg_pay, drop avg_medicare
