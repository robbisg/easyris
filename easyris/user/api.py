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
        logger.debug(request.headers)
        logger.debug(request.data)
        
        query = json.loads(request.data)
        
        message = system.do('login',
                            'user',
                            **query)
        
        username = query['username']
                
        is_authenticated = message.data['is_authenticated']
        user = message.data['user']
        qs = message.data['qs']
        message.data = qs
        
        current_app.logged_users = []
        logger.debug(current_app.logged_users)
        
        if username in current_app.logged_users:
            return message_factory(UserNotAuthenticatedHeader(message="User already logged!"), 
                                   data=None)
        
        if is_authenticated:
            login_user(user)
            g.user = user
            current_app.logged_users.append(username)      

        
        response = message_to_http(message)
        
        logger.debug("Config\n"+str(current_app.config))
        logger.debug("Session\n"+str(session))
        logger.debug(current_app.logged_users)
        
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
    
    logger.debug(session)
    
    logger.debug(g.user.username+" has logged out!")
    #current_app.logged_users.remove(g.user.username)
    logout_user()
    
    return message_to_http(message) 


