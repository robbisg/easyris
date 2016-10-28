from flask import g
from flask.ext.login import LoginManager,current_user
from flask.templating import render_template_string

<<<<<<< Updated upstream
from mongoengine import connect
from easyris.examination.api.base import examination

# TODO: Move all the configuration in a function
# TODO: as mentioned in Application factories section

#app = Flask(__name__)
app = EasyRis(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['PACS_URL'] = "http://192.168.30.225:6000/api/v1/orders"
# This is to prevent bad url in frontend
app.url_map.strict_slashes = False

# Register blueprint from other modules
app.register_blueprint(patient, url_prefix='/patient')
app.register_blueprint(cities, url_prefix='/cities')
app.register_blueprint(typology, url_prefix='/typology')
app.register_blueprint(examination, url_prefix='/examination')
app.register_blueprint(login_, url_prefix='')
app.register_blueprint(report, url_prefix="/report")

login_manager = LoginManager()
login_manager.init_app(app)

app.debug = True
# TODO: Decide about session duration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
# TODO: Keep it in the database??
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

toolbar = DebugToolbarExtension(app)
=======
from easyris import create_app
>>>>>>> Stashed changes

app = create_app("easyris.cfg")

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


@app.login_manager.user_loader
def load_user(userid):
    # Return an instance of the User model
    return app.get_user(userid)
<<<<<<< Updated upstream
    
=======
      
>>>>>>> Stashed changes


def enable_logging():
    import logging
    import logging.handlers
    logger = logging.getLogger('easyris_logger')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler('/home/vagrant/easyris.log',
                                              maxBytes=2*1024*1024,
                                              backupCount=5)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
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
    # connect('easyris')
    

    
    handler = enable_logging()
    app.logger.addHandler(handler)
    
    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True,
		    ssl_context=('/etc/webserver-ssl/webserver.crt', 
                         '/etc/webserver-ssl/webserver.key')
		  )
    
    app.toolbar.init_app(app)