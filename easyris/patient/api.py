from flask import Blueprint, jsonify, request
from model import Patient
from mongoengine import *
from utils.decorators import jsonp, crossdomain
import json
from datetime import datetime
from patient.controller import PatientController


patient = Blueprint('patient', __name__)
controller = PatientController()

connect('easyris', port=27017)


@patient.route('/<int:id>', methods=['GET'])
@jsonp
def show(id):
    query = Patient.objects(id_patient=str(id))
    #return jsonify(json.loads(query.to_json())[0])
    return jsonify(result=query.to_json())


@patient.route('/<int:id>/delete', methods=['GET', 'POST'])
@jsonp
def delete(id):
    return



@patient.route('/<int:id>/edit', methods=['GET', 'POST'])
@jsonp
def edit(id):
    return  
   
        
@patient.route('/', methods=['GET'])
@jsonp
def patient_list():
    # TODO: Rimanda nome, cognome, id, cf, telefono
    # TODO: bson or json?
    query = Patient.objects()
    response = ''
    # TODO: Include in a function code below
    for patient in query:
        response = patient.to_json()
        
    return response



@patient.route('/search', methods=['GET', 'POST', 'OPTIONS'])
@jsonp
#@crossdomain(origin='*', methods=['POST', 'OPTIONS'], 
#             headers=['X-Requested-With', 'Content-Type', 'Origin'])
def search():
    """
    Test with 
    
    curl --data "first_name=Piero" http://localhost:5000/patient/search
    """
    if request.method == 'POST':
        print request.form
        print request.headers
        patients = Patient.objects(**request.form.to_dict())
        print request.form.to_dict()
        if patients.count() == 0:
            return 'No results!'
        else:
            #TODO: Check if patient is "Attivo"
            response = ""
            for patient in patients:
                response = patient.to_json()
            
            return response


@patient.route('/insert', methods=['GET', 'POST'])
@jsonp
def insert():
    """
    Test with 
    
    curl --data "first_name=Roberto&last_name=Ruffini&gender=M&birthplace=PESCARA&
    address=Via%20Aldo%20Moro%20114&phone_number=3404752345&nationality=italiana&cap=64050
    &birthdate=12/07/1987" http://localhost:5000/patient/insert
    """
    if request.method == 'POST':
        # TODO: Check fields if they're correct!
        # TODO: Manage birthdate.
        # TODO: Check sul codice fiscale se esiste il paziente.
        query = request.form.to_dict()
        birthdate = query['birthdate'].split('/')
        query['birthdate'] = datetime(year=int(birthdate[2]),
                                      month=int(birthdate[1]),
                                      day=int(birthdate[0])
                                      )
        patient = Patient(**query)
        patient.save()
        return 'OK!'