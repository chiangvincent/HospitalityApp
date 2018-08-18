# HospitalityApp

## Overview
The Hospitality App recommends hospitals based on a user's location, hospital distances, and coverage for common major procedures. The app leverages government data on Medicare coverage for over 3000+ hospitals in the US.

## Demo
![hospitality_app_demo_sped_up](https://user-images.githubusercontent.com/33586225/44294628-f6689d00-a24e-11e8-86a2-08b8e7ad3961.gif)

## Dataset
The dataset used can be found [here] (https://data.cms.gov/Medicare-Inpatient/Inpatient-Prospective-Payment-System-IPPS-Provider/97k6-zzx3).

## Technologies Used
- **Flask** for python web framework, and **Jinja2** for python/html template engine
- **MYSQL** for database **SQLAlchemy** for database modeling and dynamic manipulation
- **JavaScript**, **HTML/CSS**, and **Bootstrap** for front-end web design
- The following **Google APIs**:
    - Distance Matrix
    - Geocoding
    - Maps JavaScript
