from flask import Flask, Blueprint, jsonify, request, Response, \
                    session, g, url_for
from flask.ext.cors import CORS, cross_origin
from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user
from flask_debugtoolbar import DebugToolbarExtension

from easyris import EasyRis
from easyris.utils.api import cities
from easyris.base.message.utils import build_response
from easyris.patient.api import patient
from easyris.user.api import login_
from easyris.examination.api.typology import typology
from easyris.utils.decorators import crossdomain, jsonp
from datetime import datetime, timedelta
import json
from flask.templating import render_template_string

from mongoengine import connect
from easyris.examination.api.base import examination

import logging
import logging.handlers

# TODO: Move all the configuration in a function
# TODO: as mentioned in Application factories section

#app = Flask(__name__)
app = EasyRis(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['LOGGED_USERS'] = []

# This is to prevent bad url in frontend
app.url_map.strict_slashes = False

# Register blueprint from other modules
app.register_blueprint(patient, url_prefix='/patient')
app.register_blueprint(cities, url_prefix='/cities')
app.register_blueprint(typology, url_prefix='/typology')
app.register_blueprint(examination, url_prefix='/examination')
app.register_blueprint(login_, url_prefix='')


login_manager = LoginManager()
login_manager.init_app(app)

app.debug = True
# TODO: Decide about session duration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
# TODO: Keep it in the database??
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

toolbar = DebugToolbarExtension(app)

@app.route('/')
def entry(): 
    return 'Flask is up!'

@app.route('/debug')
def debug():
    return render_template_string('<html><body></body></html>')


@app.before_request
def before_request():
    #app.logger.debug(request.header)
    g.user = current_user


@login_manager.user_loader
def load_user(userid):
    # Return an instance of the User model
    return app.get_user(userid)


def enable_logging():
    logger = logging.getLogger('easyris_logger')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler('/home/vagrant/easyris.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('----------\n'+
                                  '%(asctime)s - '+
                                  '%(levelname)s - '+ 
                                  '[%(pathname)s:'+
                                  '%(lineno)s] - '+
                                  '%(name)s - :\n'+
                                  '%(message)s')
    
    
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return fh



if __name__ == '__main__':
    
    # TODO: Secure connection???
    connect('easyris')
    
    handler = enable_logging()
    
    app.logger.addHandler(handler)
    
    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True,
		    ssl_context=('/etc/webserver-ssl/webserver.crt', '/etc/webserver-ssl/webserver.key')
		  )
    
    toolbar.init_app(app)