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
from flask.templating import render_template

logger = logging.getLogger("easyris_logger")

report = Blueprint('report', __name__)

# TODO: Should I start the class in easyris.app??
system = EasyRisFacade()


def _render(message):
    print message
    return render_template()




@report.route('/', methods=['GET', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['GET', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'report')
def read():
        
    if request.method == 'GET':
        
        if not g.user.is_anonymous:
            logger.info('User:'+g.user.username)
        
        query = dict()
            
        message = system.do('read',
                            'report',
                            user=g.user.username,
                            **query)
        
        response = message_to_http(message)

        return response



@report.route('/search', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'report')
def search():
        
    if request.method == 'POST':
        
        if not g.user.is_anonymous:
            logger.info('User:'+g.user.username)
        
        logger.debug(request.data)
        logger.debug(request.headers)
        
        query = json.loads(request.data)
            
        message = system.do('read',
                            'report',
                            user=g.user.username,
                            **query)
        
        response = message_to_http(message)

        return response




@report.route('/save', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('save', 'report')
def save_report():
    
    if request.method == 'POST':
        logger.debug(request.data)
        logger.debug(request.headers)
        
        query = json.loads(request.data)
        
        if 'id' in query.keys():
            action = 'update'
        else:
            action = 'create'
        
        query['action'] = action
          
        message = system.do(action,
                            'report',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)
        
        return response
    
    
@report.route('/<string:id>/close', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('close', 'report')
def close_report(id):
    
    if request.method == 'POST':
        logger.debug(request.data)
        logger.debug(request.headers)
        
        query = dict()
        query['id'] = str(id)

        message = system.do('close',
                            'report',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)
        
        return response
    

@report.route('/<string:id>/open', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('open', 'report')
def open_report(id):
    
    if request.method == 'POST':
        logger.debug(request.data)
        logger.debug(request.headers)
        
        query = json.loads(request.data)
        query['id'] = str(id)
        
        message = system.do('open',
                            'report',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)
        
        return response
    
@report.route('/<string:id>/print', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('print', 'report')
def print_report(id):
    
    if request.method == 'POST':
        logger.debug(request.data)
        logger.debug(request.headers)
        
        query = dict()
        query['id'] = str(id)
        message = system.do('print_report',
                            'report',
                            user=g.user.username,
                            **query)

        response = _render(message)
        
        return response


@report.route('/patient/<string:id>/<string:status>', methods=['GET', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['GET', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'report')
def patient_report(id):
    
    if request.method == 'GET':
        logger.debug(request.data)
        logger.debug(request.headers)
        
        query = dict()
        query['id'] = str(id)
        message = system.do('print_report',
                            'report',
                            user=g.user.username,
                            **query)

        response = _render(message)
        
        return response