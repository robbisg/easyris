from easyris import EasyRis
from easyris.base.middleware import build_response
from flask.ext.cors import CORS, cross_origin
from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user
from flask import request, Response, session, g, Blueprint
import json


login_ = Blueprint('login', __name__)
     
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
        
        
        print request.headers
        #print request.headers['Origin']
        #print request.data
        #print request.form
        
        query = json.loads(request.data)
        username = query['username']
        password = query['password']
        
        is_authenticated, user = EasyRis.login(username, password)
        
        if is_authenticated:
            login_user(user)
            g.user = user
            print user.roles
            response = build_response([user])
        else:
            response = Response(response='NO!',
                        status=200,
                        #mimetype="application/json"
                        )
                
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
    logout_user()
    return 'Logged out!'

