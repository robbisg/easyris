from flask import Blueprint, jsonify, request, Response, g
from easyris.base.controller import EasyRisFacade
from flask_cors.decorator import cross_origin
from flask_login import login_required, current_user
from easyris.utils.decorators import has_permission, jsonp, crossdomain
from easyris.base.message.utils import build_response, message_to_http
import json

examination = Blueprint('examination', __name__)


# TODO: Should I start the class in easyris.app??
system = EasyRisFacade()



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
    
    # TODO: Log stuff!
    print request.headers
    if not g.user.is_anonymous:
        print 'User:'+g.user.username

    if request.method == 'GET':

        query = dict()

        message = system.do('read',
                            'examination',
                            user=g.user.username,
                            **query)


        response = message_to_http(message)

        return response

@examination.route('/<int:id>', methods=['GET', 'POST', 'OPTIONS'])
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

@examination.route('/<int:id>/delete', methods=['POST', 'OPTIONS'])
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
        query = request.form.to_dict()

        status = query['status']
        note = query['note']
        message = system.do('delete',
                            'examination',
                            user=g.user.username,
                            status=status,
                            note=note)

        response = message_to_http(message)

    return response

@examination.route('/<int:id>/edit', methods=['POST', 'OPTIONS'])
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

        query = request.form.to_dict()
        query['id'] = id

        message = system.do('update',
                            'examination',
                            user=g.user.username,
                            **query)

        response = message_to_http(message)

    return response

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

        print request.data
        print request.headers

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

        print request.data
        print request.headers

        query = json.loads(request.data)

        message = system.do('create',
                            'examination',
                            user=g.user.username,
                            **query)

        print message
        response = message_to_http(message)

        return response

