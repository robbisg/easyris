from flask import Flask, Blueprint, jsonify, request, Response, \
                    session, g, url_for
from flask.ext.cors import CORS, cross_origin
from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user
from flask_debugtoolbar import DebugToolbarExtension

from easyris import EasyRis
from easyris.utils.api import cities
from easyris.base.middleware import build_response
from easyris.patient.api import patient
from easyris.user.api import login_
from easyris.utils.decorators import crossdomain, jsonp

import json
from flask.templating import render_template_string

from mongoengine import connect

#import cryptography
#from OpenSSL import crypto
#from OpenSSL import SSL
#import os
#context = SSL.SSLContext(SSL.PROTOCOL_TLSv1_2)
#context.load_cert_chain('/etc/webserver-ssl/webserver.crt','/etc/webserver-ssl/webserver.key')
#cer = os.path.join(os.path.dirname(__file__), '/etc/webserver-ssl/webserver.crt')
#key = os.path.join(os.path.dirname(__file__), '/etc/webserver-ssl/webserver.key')
 


# TODO: Move all the configuration in a function
# TODO: as mentioned in Application factories section

#app = Flask(__name__)
app = EasyRis(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False
# This is to prevent bad url in frontend
app.url_map.strict_slashes = False

# Register blueprint from other modules
app.register_blueprint(patient, url_prefix='/patient')
app.register_blueprint(cities, url_prefix='/cities')
app.register_blueprint(login_, url_prefix='')


login_manager = LoginManager()
login_manager.init_app(app)

app.debug = True

# TODO: Keep it in the database??
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

toolbar = DebugToolbarExtension(app)

@app.route('/')
def entry(): 
    return render_template_string('<html><body></body></html>')


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(userid):
    # Return an instance of the User model
    return app.get_user(userid)




if __name__ == '__main__':
    connect('easyris')
    
    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True,
		    ssl_context=('/etc/webserver-ssl/webserver.crt', '/etc/webserver-ssl/webserver.key')
		  )
    
    toolbar.init_app(app)