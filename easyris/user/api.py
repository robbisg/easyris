from easyris.base.message.utils import message_to_http
from flask.ext.cors import CORS, cross_origin
from easyris.base.controller import EasyRisFacade
from flask.ext.login import LoginManager, login_user, \
                    logout_user, login_required, current_user
from flask import request, session, g, Blueprint, current_app
import json
import logging
from easyris.base.message.message import message_factory
from easyris.user.message import UserNotAuthenticatedHeader

logger = logging.getLogger('easyris_logger')
login_ = Blueprint('login', __name__)

system = EasyRisFacade()

@login_.route('/user')
@login_required
def user():
    return 'Hello '+g.user.username+'!'


@login_.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origin=None, 
              methods=['POST', 'OPTIONS'], 
              allow_headers=['X-Requested-With', 
                            'Content-Type', 
                            'Origin'],
              supports_credentials=True)
def login():

    if request.method == 'POST':

        logger.debug(request.data)
        
        query = json.loads(request.data)
        
        message = system.do('login',
                            'user',
                            **query)
        
                
        is_authenticated = message.data['is_authenticated']
        user = message.data['user']
        qs = message.data['qs']
        message.data = qs
        
        if is_authenticated:
            login_user(user)
            g.user = user  

        response = message_to_http(message)
        
        return response


@login_.route('/logout', methods=['GET'])
@cross_origin(origin=None, 
              methods=['POST', 'OPTIONS'], 
              allow_headers=['X-Requested-With', 
                      'Content-Type', 
                      'Origin'],
              supports_credentials=True)
@login_required
def logout():
    
    if request.method == 'GET':
        query = dict()
        query['user'] = g.user.username
        message = system.do('logout',
                            'user',
                            **query)
    
    
    logger.debug(g.user.username+" has logged out!")
    logout_user()
    
    return message_to_http(message) 

@login_.route('/password', methods=['POST', 'OPTIONS'])
@cross_origin(origin=None, 
              methods=['POST', 'OPTIONS'], 
              allow_headers=['X-Requested-With', 
                      'Content-Type', 
                      'Origin'],
              supports_credentials=True)
@login_required
def modify_password():
    return