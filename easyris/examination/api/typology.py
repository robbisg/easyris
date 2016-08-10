from flask import Blueprint, jsonify, request, Response, g
from easyris.base.controller import EasyRisFacade
from flask_cors.decorator import cross_origin
from flask_login import login_required, current_user
from easyris.utils.decorators import has_permission, jsonp, crossdomain
from easyris.base.message.utils import build_response, message_to_http


typology = Blueprint('typology', __name__)
system = EasyRisFacade()

@typology.route('/', methods=['GET', 'OPTIONS'])
@cross_origin(origin=None,
              methods=['GET', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
@login_required
@has_permission('read', 'patient') # Who is?
def get_typology():
    # TODO: Log stuff!
    print request.headers
    if not g.user.is_anonymous:
        print 'User:'+g.user.username

    if request.method == 'GET':

        query = dict()

        message = system.do('read',
                            'typology',
                            user=g.user.username,
                            **query)


        response = message_to_http(message)

        return response
