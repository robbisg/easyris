from flask import Blueprint, jsonify, request, Response

from mongoengine import *
from bson.json_util import dumps
import json
from datetime import datetime

from controller import PatientController
from utils.decorators import jsonp, crossdomain
from easyris.utils.response import build_response

patient = Blueprint('patient', __name__)
controller = PatientController()


@patient.route('/<int:id>', methods=['GET'])
@jsonp
def show(id):
    message = controller.get_patient(id)
    print message
    if message == 'ERR':
        return "Patient not found"
        
    return build_response(message)


@patient.route('/<int:id>/delete', methods=['GET', 'POST'])
@jsonp
@crossdomain(origin='*', methods=['POST', 'OPTIONS'], 
             headers=['X-Requested-With', 'Content-Type', 'Origin'])
def delete(id):
    if request.method == 'POST':
        query = request.form.to_dict()
        # TODO: Check if they exist?!?!
        # TODO: Is it good to extract fields from request?
        status = query['status']
        note = query['note']
        message = controller.delete(status, note)
    return message



@patient.route('/<int:id>/edit', methods=['POST', 'OPTIONS'])
@jsonp
@crossdomain(origin='*', methods=['POST', 'OPTIONS'], 
             headers=['X-Requested-With', 'Content-Type', 'Origin'])
def edit(id):
    
    if request.method == 'POST':
        query = request.form.to_dict()
        # TODO: Check if they exist?!?!
        message = controller.update(**query)
    return message

   
        
@patient.route('/', methods=['GET'])
@jsonp
def get_patients():
    # TODO: Rimanda nome, cognome, id, cf, telefono
    # TODO: bson or json?
    if request.method == 'GET':
        print request
        query = dict()
        message = controller.search(**query)
        
        if message == None:
            return Response(response='No patient in database',
                            status=410)
            
        return build_response(message)


@patient.route('/search', methods=['POST', 'OPTIONS'])
@jsonp
@crossdomain(origin='*', methods=['POST', 'OPTIONS'], 
             headers=['X-Requested-With', 'Content-Type', 'Origin'])
def search():
    """
    Test with 
    curl -H "Content-Type: application/json" 
    -X POST -d '{"first_name":"Tecla"}' 
    http://localhost:5000/patient/search
    curl --data "first_name=Piero" http://localhost:5000/patient/search
    """
    if request.method == 'POST':

        print request.data
        print request.headers
        
        query = json.loads(request.data)
          
        message = controller.search(**query)
        
    return build_response(message)
        


@patient.route('/insert', methods=['POST', 'OPTIONS'])
@jsonp
@crossdomain(origin='*', methods=['POST', 'OPTIONS'], 
             headers=['X-Requested-With', 'Content-Type', 'Origin'])
def insert():
    """
    Test with 
    
    curl --data "first_name=Roberto&last_name=Guidotti&gender=M&birthplace=PESCARA&
    address=Via%20Aldo%20Moro%20114&phone_number=3404752345&nationality=italiana&cap=64050
    &birthdate=12/07/1987" http://localhost:5000/patient/insert
    """
    if request.method == 'POST':
        
        print request.data
        print request.headers
        
        query = json.loads(request.data)
        message = controller.create(**query)
        print message
        return message