from easyris import EasyRis
from easyris.base.message.utils import message_to_http
from flask.ext.cors import CORS, cross_origin
from easyris.base.controller import EasyRisFacade
from flask.ext.login import LoginManager, login_user, \
                    logout_user, login_required, current_user
from flask import request, session, g, Blueprint, current_app, \
            _app_ctx_stack, _request_ctx_stack
import json
import logging
from flask.globals import _app_ctx_stack, _request_ctx_stack

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
        logger.debug(_app_ctx_stack.top)
        logger.debug(_request_ctx_stack.top)
        logger.debug(request.headers)
        logger.debug(request.data)
        
        query = json.loads(request.data)
        
        message = system.do('login',
                            'user',
                            **query)
        
        username = query['username']
        
        logger.debug(message.data)
        
        is_authenticated = message.data['is_authenticated']
        user = message.data['user']
        qs = message.data['qs']
        message.data = qs
        
        logger.debug(message.data)

        if is_authenticated:
            login_user(user)
            g.user = user
            # TODO: Is there a better way to deal with it?
            #current_app.config['LOGGED_USERS'].append(username)
        
        response = message_to_http(message)
        
        logger.debug("Config\n")
        logger.debug(current_app.config)
        logger.debug("Session\n")
        logger.debug(session)

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
    
    if request.method == 'POST':
        query = dict()
        message = system.do('login',
                            'user',
                            **query)
    
    logger.debug(session)
    
    logger.debug(g.user.username+" has logged out!")
    logout_user()
    return 'Logged out!'

