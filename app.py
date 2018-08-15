from flask import Flask, render_template, request
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from gmaps import get_state, get_geocode, get_distance


# engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)
#163065 = num rows of table
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Database123@localhost/hospitalityapp'
db = SQLAlchemy(app)

app.debug = True
db.init_app(app)

@app.route('/')
def home():
    from models import Hospitals
    return render_template('home.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        procedure = request.form['myInput']
        address = request.form['address']
        geocode = get_geocode(address)
        state = get_state(geocode)
        #state_list is a queried object of SQLAlchemy
        state_list = find_closest(state, procedure)
        session = add_distance(state_list, address)
        find_closest_local(session, state_list)
        return "Hi"

#HELPER FUUNCTIONS AND DATA STRUCUTRES
procedures = {
        "Extracranial Procedure" : "039 - EXTRACRANIAL PROCEDURES W/O CC/MCC",
        "Intracranial Hemorrhage or Cerebral Infarction" : "066 - INTRACRANIAL HEMORRHAGE OR CEREBRAL INFARCTION W/O CC/MCC",
        "Degenerative Nervous System Disorder" : "057 - DEGENERATIVE NERVOUS SYSTEM DISORDERS W/O MCC",
        "Transient Ischemia" : "069 - TRANSIENT ISCHEMIA",
        "Cranial or Peripheral Nerve Disorder" : "074 - CRANIAL & PERIPHERAL NERVE DISORDERS W/O MCC",
        "Seizure" : "101 - SEIZURES W/O MCC",
        "Dysequilibirum" : "149 - DYSEQUILIBRIUM",
        "Pulmonary Embolism" : "176 - PULMONARY EMBOLISM W/O MCC",
        "Respiratory Infection or Inflammation" : "178 - RESPIRATORY INFECTIONS & INFLAMMATIONS W CC",
        "Pulmonary Edema or Respiratory Failure" : "189 - PULMONARY EDEMA & RESPIRATORY FAILURE",
        "Chronic Obstructive Pulmonary Disease" : "191 - CHRONIC OBSTRUCTIVE PULMONARY DISEASE W CC",
        "Pneumonia and Pleurisy" : "194 - SIMPLE PNEUMONIA & PLEURISY W CC",
        "Bronchitis and Asthma" : "203 - BRONCHITIS & ASTHMA W/O CC/MCC",
        "Respiratory System Diagnosis with Ventilator Support" : "207 - RESPIRATORY SYSTEM DIAGNOSIS W VENTILATOR SUPPORT 96+ HOURS",
        "Major Cardiovascular Procedure" : "238 - MAJOR CARDIOVASC PROCEDURES W/O MCC",
        "Acute Myocardial Infarction" : "282 - ACUTE MYOCARDIAL INFARCTION, DISCHARGED ALIVE W/O CC/MCC",
        "Permanent Cardiac Pacemaker Implant" : "244 - PERMANENT CARDIAC PACEMAKER IMPLANT W/O CC/MCC",
        "Circulatory Disorders" : "287 - CIRCULATORY DISORDERS EXCEPT AMI, W CARD CATH W/O MCC",
        "Heart Failure or Shock" : "293 - HEART FAILURE & SHOCK W/O CC/MCC",
        "Peripheral Vascular Disorder" : "301 - PERIPHERAL VASCULAR DISORDERS W/O CC/MCC",
        "Atherosclerosis" : "303 - ATHEROSCLEROSIS W/O MCC",
        "Hypertension" : "305 - HYPERTENSION W/O MCC",
        "Cardiac Arrhythmia or Conduction Disorder" : "310 - CARDIAC ARRHYTHMIA & CONDUCTION DISORDERS W/O CC/MCC",
        "Chest Pain" : "313 - CHEST PAIN",
        "Major Small or Large Bowel Procedure" : "329 - MAJOR SMALL & LARGE BOWEL PROCEDURES W MCC",
        "Major Gastrointestinal Disorder or Peritoneal Infection" : "372 - MAJOR GASTROINTESTINAL DISORDERS & PERITONEAL INFECTIONS W CC",
        "Gastrointestinal Hemorrhage" : "377 - G.I. HEMORRHAGE W MCC",
        "Gastrointestinal Obstructions" : "390 - G.I. OBSTRUCTION W/O CC/MCC",
        "Esophagitis, Gastrointestinal or Misc. Digestive Disorders" : "391 - ESOPHAGITIS, GASTROENT & MISC DIGEST DISORDERS W MCC",
        "Laparoscopic Cholecystectomy" : "419 - LAPAROSCOPIC CHOLECYSTECTOMY W/O C.D.E. W/O CC/MCC",
        "Disorders of Pancreas" : "439 - DISORDERS OF PANCREAS EXCEPT MALIGNANCY W CC",
        "Spinal Fusion" : "460 - SPINAL FUSION EXCEPT CERVICAL W/O MCC",
        "Major Joint Replacement or Reattachment" : "470 - MAJOR JOINT REPLACEMENT OR REATTACHMENT OF LOWER EXTREMITY W/O MCC",
        "Cervical Spinal Fusion" : "473 - CERVICAL SPINAL FUSION W/O CC/MCC",
        "Fractures of Hip and Pelvis" : "536 - FRACTURES OF HIP & PELVIS W/O MCC",
        "Cellulitis" : "603 - CELLULITIS W/O MCC",
        "Misc. Disorders of Nutrition/Metabolism/Electrolytes" :"641 - MISC DISORDERS OF NUTRITION,METABOLISM,FLUIDS/ELECTROLYTES W/O MCC",
        "Renal Failure" : "684 - RENAL FAILURE W/O CC/MCC",
        "Kidney and Urinary Tract Infection" : "690 - KIDNEY & URINARY TRACT INFECTIONS W/O MCC",
        "Red Blood Cell Disorders" : "812 - RED BLOOD CELL DISORDERS W/O MCC",
        "Infectious and Parasitic Diseases" : "853 - INFECTIOUS & PARASITIC DISEASES W O.R. PROCEDURE W MCC",
        "Septicemia or Severe Sepsis" : "872 - SEPTICEMIA OR SEVERE SEPSIS W/O MV 96+ HOURS W/O MCC",
        "Psychoses" : "885 - PSYCHOSES",
        "Alcohol/Drug Abuse or Rehabilitation Therapy" : "897 - ALCOHOL/DRUG ABUSE OR DEPENDENCE W/O REHABILITATION THERAPY W/O MCC",
        "Poisoning and Toxic Effects of Drugs" : "918 - POISONING & TOXIC EFFECTS OF DRUGS W/O MCC",
        "Signs and Symptoms Checkup" : "948 - SIGNS & SYMPTOMS W/O MCC",
}


#returns top 10 closest hospitals from database
#state is string of the state of entered address
#drg is the non-converted code
#test using drg = "Extracranial Procedure"
# def find_closest(state, drg):
#     from models import Hospitals
#     drg = procedures[drg]
#     in_state =  Hospitals.query.filter_by(drg = drg).filter_by(state = state).all()
#     return in_state

def find_closest(state, drg):
    from models import Hospitals
    drg = procedures[drg]
    in_state =  Hospitals.query.filter_by(drg = drg).filter_by(state = state).all()
    for hospital in in_state:
        print(hospital)
    return in_state

def find_closest_local(session, query_object):
    from models import HospitalsDistance
    sub_q = session.query(HospitalsDistance).order_by(HospitalsDistance.distance).limit(10).subquery()
    a = session.query(HospitalsDistance, sub_q).order_by('anon_1.avg_covered DESC').limit(3).all()
    return a

#adds distance to a given SQLAlchemy table from a starting location (String)
#queried hospitals has been filtered for the same drg and same state
#add_distance creates new table that adds distance from specified location
def add_distance(queried_hospitals, location):
    from models import create_distance_table
    session = create_distance_table()
    #importing the new class after the session table has been created
    from models import HospitalsDistance
    #state_list is a query object
    i = 0
    for hospital in queried_hospitals:
        if hospital is not None:
            address = hospital.address + " " + hospital.city + " " + hospital.state
            print(address)
            distance = get_distance(location, address)
            hospital_w_distance = HospitalsDistance(i, hospital.name, address, hospital.avg_covered, distance)
            session.add(hospital_w_distance)
            i += 1
    return session

# at the bottom to run the app
if __name__ == '__main__':
    # session = scoped_session(sessionmaker(bind=engine))
    app.run()
