from flask import Blueprint, request, g, Response
from flask.templating import render_template
from flask_cors.decorator import cross_origin
from flask_login import login_required
from easyris.base.controller import EasyRisFacade
from easyris.base.message.utils import message_to_http
from easyris.base.async import save_pdf
from easyris.utils.decorators import has_permission, jsonp
import json
import logging


logger = logging.getLogger("easyris_logger")

report = Blueprint('report', __name__)

# TODO: Should I start the class in easyris.app??
system = EasyRisFacade()



def _render(message):

    html_ = render_template("RefertoTemplate.html", **message)

    #logger.debug(str(html_).__class__)
    save_pdf.delay(html_, message['report_id']+'.pdf')

    

    return Response(response=json.dumps({'data':html_}),
                        status=200,
                        mimetype="application/json")


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
        
        logger.debug(request.data)
        
        query = json.loads(request.data)
            
        message = system.do('read',
                            'report',
                            user=g.user.username,
                            **query)
        
        response = message_to_http(message)

        return response
    
    
@report.route('/<string:id>/delete', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('create', 'report')
def delete_report(id):
    
    if request.method == 'POST':
        
        query = dict()
        query['id'] = str(id)
          
        message = system.do('delete',
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
        
        if query['password'] == '':
            query = dict()
        
        query['id'] = str(id)
        
        message = system.do('open',
                            'report',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)
        
        return response


@report.route('/<string:id>/pause', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('open', 'report') # Va bene!
def pause_report(id):
    
    if request.method == 'POST':
        logger.debug(request.headers)
        
        query = dict()
        query['id'] = str(id)
        
        message = system.do('pause',
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
        logger.debug(request.headers)
        
        query = dict()
        query['id'] = str(id)
        message = system.do('print_report',
                            'report',
                            user=g.user.username,
                            **query)
        logger.debug(message.data)
        response = _render(message.data)        
        #response = message_to_http(message)
        
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
def patient_report(id, status):
    
    if request.method == 'GET':
        
        query = dict()
        query['id_patient'] = str(id)
        query['status_name'] = str(status)
        message = system.do('read',
                            'report',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)
        
        return response