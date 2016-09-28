from easyris import EasyRis
from easyris.base.message.utils import message_to_http
from flask.ext.cors import CORS, cross_origin
from easyris.base.controller import EasyRisFacade
from flask.ext.login import LoginManager, login_user, \
                    logout_user, login_required, current_user
from flask import request, Response, session, g, Blueprint, current_app
import json
import logging

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
        
        logged_users = current_app.config['LOGGED_USERS']
        
        #if username in logged_users:
            #response = Response()
        
        # TODO: I dislike it!
        message = system.do('login',
                            'user',
                            **query)
        
        username = query['username']
        #password = query['password']
        #is_authenticated, user = EasyRis.login(username, password)
        
        logger.debug(message.data)
        
        is_authenticated = message.data['is_authenticated']
        user = message.data['user']
        qs = message.data['qs']
        message.data = qs
        
        logger.debug(message.data)

        if is_authenticated and not username in logged_users:
            login_user(user)
            g.user = user
            # TODO: Is there a better way to deal with it?
            #current_app.config['LOGGED_USERS'].append(username)
        
        response = message_to_http(message)
        
        logger.debug(current_app.config)
        #logger.debug(session['_id'])

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
    
    # TODO: Pop user logged out from app variables
    logger.debug(g.user.username+" has logged out!")
    logout_user()
    return 'Logged out!'

