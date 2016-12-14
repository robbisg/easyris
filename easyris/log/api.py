from flask import Blueprint, request, g
from easyris.base.controller import EasyRisFacade
from flask_cors.decorator import cross_origin
from flask_login import login_required
from easyris.utils.decorators import has_permission, jsonp
from easyris.base.message.utils import message_to_http
from easyris.base.message import message_factory
from easyris.base.message.error import NotImplementedApiHeader
from easyris.log import store_event
import json
import logging
from datetime import datetime


event = Blueprint('event', __name__)


@event.route('/', methods=['GET','POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['GET', 'POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
def post_event():
    
    if request.method == 'GET':
        
        print str(request)
        print request.headers
        print request.user_agent
        print request.remote_addr
        print request.referrer
        #query = json.loads(request.data)
        
        message = store_event()
        
        #response = message_to_http(message)
        return str(request.environ['REMOTE_ADDR'])