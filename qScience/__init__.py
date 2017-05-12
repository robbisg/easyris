import sys, os
sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
__version__ = '0.9.0'

from qScience.base import QScience
from qScience.log import enable_logging

from flask import render_template_string, g
from flask_login import LoginManager,current_user




def entry():
    return 'Flask is on fire!'


def debug():
    return render_template_string('<html><body></body></html>')


def before_request():
    #app.logger.debug(request.header)
    g.user = current_user
    


def create_app(config_filename="config/easyris.cfg", 
                database_cfg="config/database.cfg",
                logger=True,
                **kwargs):
    
    app = QScience(__name__)
    app.config.from_pyfile(config_filename)
    
    kwargs = {k.upper(): v for k, v in kwargs.iteritems()}
    app.config.update(**kwargs)

    from datetime import timedelta
    session_time = app.config['PERMANENT_SESSION_LIFETIME']
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=int(session_time))

    # This is to prevent bad url in frontend
    app.url_map.strict_slashes = False
    
    
    # Add basic apis
    app.add_url_rule('/', 'entry', entry)
    app.add_url_rule('/debug', 'debug', debug)
    
    
    from qScience.api.cities import cities
    from qScience.api.patient import patient
    from qScience.api.user import login_
    from qScience.api.examination_type import typology
    from qScience.api.report import report
    from qScience.api.examination import examination
    from qScience.log.api import event
    
    
    # Register blueprint from other modules
    app.register_blueprint(patient, url_prefix='/patient')
    app.register_blueprint(cities, url_prefix='/cities')
    app.register_blueprint(typology, url_prefix='/typology')
    app.register_blueprint(examination, url_prefix='/examination')
    app.register_blueprint(login_, url_prefix='')
    app.register_blueprint(report, url_prefix="/report")
    app.register_blueprint(event, url_prefix="/event")
    
    
    from flask_debugtoolbar import DebugToolbarExtension
    app.toolbar = DebugToolbarExtension(app)
    
    app.login_manager = LoginManager()
    app.login_manager.init_app(app)
    
    app.before_request(before_request)
    
    
    def load_user(userid):
        # Return an instance of the User model
        return app.get_user(userid)
    
    app.login_manager.user_loader(load_user)
    
    
    # Database connection
    from qScience.database.base import parse_db_config, easyris_connect
    db_config = parse_db_config(database_cfg)
    db_client = easyris_connect(**db_config)
    app.config['DB_CLIENT'] = db_client
    
    if logger:
        handler = enable_logging()
        app.logger.addHandler(handler)
    
    return app
    