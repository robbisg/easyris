from flask import Blueprint, jsonify, request, Response, g
from mongoengine import *
from bson.json_util import dumps
import json
from datetime import datetime

from controller import PatientController
from easyris.base.message.utils import build_response, message_to_http
from flask_login import login_required, current_user
from flask_cors.decorator import cross_origin
from easyris.base.controller import EasyRisFacade
from easyris.utils.decorators import has_permission, jsonp, crossdomain


patient = Blueprint('patient', __name__)


# TODO: Should I start the class in easyris.app??
system = EasyRisFacade()
controller = PatientController()


# TODO: Implement the confirmation of patient data!

@patient.route('/', methods=['GET', 'OPTIONS'])
@cross_origin(origin=None, 
             methods=['GET', 'OPTIONS'], 
             allow_headers=['X-Requested-With', 
                            'Content-Type', 
                            'Origin'],
             supports_credentials=True)
@login_required
@has_permission('read', 'patient')
def get_patients():
    # TODO: Rimanda nome, cognome, id, cf, telefono
    # TODO: Log stuff!
    print request.headers
    if not g.user.is_anonymous:
        print 'User:'+g.user.username
    
    if request.method == 'GET':
        
        query = dict()
        
        message = system.do('read', 
                            'patient', 
                            user=g.user.username,
                            **query)


        response = message_to_http(message)

        return response


#TODO: Is correct to have int as id??
@patient.route('/<int:id>', methods=['GET', 'POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None, 
             methods=['GET', 'POST', 'OPTIONS'], 
             allow_headers=['X-Requested-With', 
                            'Content-Type', 
                            'Origin'],
             supports_credentials=True)
@login_required
@has_permission('read', 'patient')
def show(id):
    
    if request.method == 'GET':
                
        message = system.do('read', 
                            'patient', 
                            user=g.user.username, 
                            id_patient=id)
        
        
        response = message_to_http(message)        
        return response
    
    if request.method == 'POST':
        # What is this??
        return message



@patient.route('/<int:id>/delete', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None, 
             methods=['POST', 'OPTIONS'], 
             allow_headers=['X-Requested-With', 
                            'Content-Type', 
                            'Origin'],
             supports_credentials=True)
@login_required
@has_permission('delete', 'patient')
def delete(id):
    
    if request.method == 'POST':
        query = request.form.to_dict()
        # TODO: Check if they exist?!?!
        # TODO: Is it good to extract fields from request?
        status = query['status']
        note = query['note']
        message = system.do('delete', 
                            'patient',
                            user=g.user.username,
                            status=status, 
                            note=note)

        response = message_to_http(message)
        
    return response
    


@patient.route('/<int:id>/edit', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None, 
             methods=['POST', 'OPTIONS'], 
             allow_headers=['X-Requested-With', 
                            'Content-Type', 
                            'Origin'],
             supports_credentials=True)
@login_required
@has_permission('update', 'patient')
def update(id):
    
    if request.method == 'POST':
        
        query = request.form.to_dict()
        query['id'] = id

        message = system.do('update', 
                            'patient', 
                            user=g.user.username,
                            **query)
        
        response = message_to_http(message)
        
    return response

   

@patient.route('/search', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None, 
             methods=['POST', 'OPTIONS'], 
             allow_headers=['X-Requested-With', 
                            'Content-Type', 
                            'Origin'],
             supports_credentials=True)
@login_required
@has_permission('read', 'patient')
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

        message = system.do('read', 
                            'patient', 
                            user=g.user.username,
                            **query)
        
        response = message_to_http(message)
        
    return response
        


@patient.route('/insert', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None, 
             methods=['POST', 'OPTIONS'], 
             allow_headers=['X-Requested-With', 
                            'Content-Type', 
                            'Origin'],
             supports_credentials=True)
@login_required
@has_permission('create', 'patient')
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

        message = system.do('create', 
                            'patient', 
                            user=g.user.username,
                            **query)
        
        print message
        response = message_to_http(message)
        
        return response
    