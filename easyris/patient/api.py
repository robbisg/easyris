from flask import Blueprint, request, g
import json
import logging
from easyris.patient.controller import PatientController
from easyris.base.message.utils import message_to_http
from easyris.base.controller import EasyRisFacade
from easyris.utils.decorators import has_permission, jsonp
from flask_login import login_required
from flask_cors.decorator import cross_origin

patient = Blueprint('patient', __name__)
logger = logging.getLogger("easyris_logger")

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
    logger.debug(request.headers)
    
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
                            id_patient=str(id))
        
        
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
        query = json.loads(request.data)
        logger.debug(query)
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

        query = json.loads(request.data)
        logger.debug(query)
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

        logger.debug(request.data)
        logger.debug(request.headers)
        
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
        
        logger.debug(request.data)
        logger.debug(request.headers)
        
        query = json.loads(request.data)

        message = system.do('create', 
                            'patient', 
                            user=g.user.username,
                            **query)
        
        
        
        
        response = message_to_http(message)
        
        return response
    