from flask import Blueprint, request, g
from easyris.base.controller import EasyRisFacade
from flask_cors.decorator import cross_origin
from flask_login import login_required
from easyris.utils.decorators import has_permission, jsonp
from easyris.base.message.utils import message_to_http
from easyris.base.message import message_factory
from easyris.base.message.error import NotImplementedApiHeader
import json
import logging
from datetime import datetime

logger = logging.getLogger("easyris_logger")

examination = Blueprint('examination', __name__)

# TODO: Should I start the class in easyris.app??
system = EasyRisFacade()


def state_funcion(name, id):
    
    query = dict()
    query['id'] = id

    message = system.do(name,
                        'examination',
                        user=g.user.username,
                        **query)

    response = message_to_http(message)

    return response


def not_implemented(username):
            
    message = message_factory(NotImplementedApiHeader(user=username), 
                              data=None)
    
    response = message_to_http(message)

    return response

    

@examination.route('/', methods=['GET', 'OPTIONS'])
@cross_origin(origin=None,
              methods=['GET', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'examination')
def get_examinations():
    
    
    if not g.user.is_anonymous:
        logger.info('User:'+g.user.username)

    if request.method == 'GET':

        query = dict()

        message = system.do('read',
                            'examination',
                            user=g.user.username,
                            **query)


        response = message_to_http(message)

        return response



@examination.route('/today', methods=['GET', 'OPTIONS'])
@cross_origin(origin=None,
              methods=['GET', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'examination')
def get_today_examinations():
    
    if request.method == 'GET':

        query = dict()
        
        now = datetime.now()
        query['data_inserimento'] = datetime(day=now.day,
                                             month=now.month,
                                             year=now.year)
        
        message = system.do('read',
                            'examination',
                            user=g.user.username,
                            **query)


        response = message_to_http(message)

        return response



@examination.route('/<string:id>', methods=['GET', 'POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['GET', 'POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'examination')
def show(id):

    if request.method == 'GET':

        message = system.do('read',
                            'examination',
                            user=g.user.username,
                            id_examination=id)
        #TODO id_examination equivale al id di mongodb riguardante l'esame

        response = message_to_http(message)
        return response

    if request.method == 'POST':
        # What is this??
        return message

@examination.route('/<string:id>/delete', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('delete', 'examination')
def delete(id):

    if request.method == 'POST':
        return not_implemented(g.user.username)

@examination.route('/<string:id>/edit', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('update', 'examination')
def update(id):

    if request.method == 'POST':
        return not_implemented(g.user.username)

@examination.route('/search', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'examination')
def search():
    """
    Test with
    """
    if request.method == 'POST':

        logger.debug(request.data)
        logger.debug(request.headers)

        query = json.loads(request.data)
        
        message = system.do('read',
                            'examination',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)

    return response

@examination.route('/insert', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('create', 'examination')
def insert():
    """
    Test with
    """

    if request.method == 'POST':

        logger.debug(request.data)
        logger.debug(request.headers)
        
        query = json.loads(request.data)
        
        query['id_creator'] = g.user.username
        
        logger.debug('Examination list: ' + str(query['exams']))
        
        message = system.do('create',
                            'examination',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)
        
        
        return response


@examination.route('/patient/<int:id>', methods=['GET', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['GET', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'examination')
def show_patient_examinations(id):
    
    if request.method == 'GET':

        query = dict()
        query['id_patient'] = str(id)

        message = system.do('read',
                            'examination',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)

        return response



@examination.route('/patient/<int:id>/<string:status>', methods=['GET', 'POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['GET', 'POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'examination')
def show_patient_status_examinations(id, status):
    
    if request.method == 'GET' or request.method == 'POST':
         
        query = dict()
        query['id_patient'] = str(id)
        
        if request.method == 'POST':
            logger.debug(request.data)
            logger.debug(request.headers)
        
            data = json.loads(request.data)
            
            if 'data_inserimento' in data.keys():
                # Voglio solo la data!
                # Do o' rest... Nun me ne fott nu cazz! :)
                query['data_inserimento'] = data['data_inserimento']
        
        
        if status in _get_status_list():
            query['status_name'] = status
        else:
            message = "Status %s forbidden" % (status)
            logger.error("User "+g.user.username+": "+message)
            msg = message_factory(header=NotImplementedApiHeader(message=message,
                                                                 user=g.user.username), 
                                   data=None)
            return message_to_http(msg)

        message = system.do('read',
                            'examination',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)

        return response
        
        

@examination.route('/<string:id>/start', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission("start", 'examination')
def start(id):
    
    if request.method == 'POST':
        
        response = state_funcion('start', id)

        return response
    


@examination.route('/<string:id>/go', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('go', 'examination')
def go(id):
    
    if request.method == 'POST':
        
        response = state_funcion('go', id)

        return response


@examination.route('/<string:id>/stop', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('stop', 'examination')
def stop(id):
    
    if request.method == 'POST':
        
        response = state_funcion('stop', id)

        return response


@examination.route('/<string:id>/pause', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('pause', 'examination')
def pause(id):
    if request.method == 'POST':
        
        response = state_funcion('pause', id)

        return response


@examination.route('/<string:id>/finish', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('finish', 'examination')
def finish(id):
    if request.method == 'POST':
        
        response = state_funcion('finish', id)

        return response



@examination.route('/<string:id>/eject', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('eject', 'examination')
def eject(id):
    if request.method == 'POST':
        
        response = state_funcion('eject', id)

        return response



def _get_status_list():
    return ['new',
            'scheduled',
            'running',
            'rescheduled',
            'completed',
            'incompleted',
            'reported']