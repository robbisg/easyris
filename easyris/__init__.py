import sys, os
sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
__version__ = '0.9.0'

from easyris.base import EasyRis

<<<<<<< Updated upstream
class EasyRis(Flask):
    ## Should be a Singleton??
    
    def __init__(self, import_name, static_path=None, static_url_path=None, 
        static_folder='static', template_folder='templates', 
        instance_path=None, instance_relative_config=False):
                
        Flask.__init__(self, 
                       import_name, 
                       static_path=static_path, 
                       static_url_path=static_url_path, 
                       static_folder=static_folder, 
                       template_folder=template_folder, 
                       instance_path=instance_path, 
                       instance_relative_config=instance_relative_config)
            
    @staticmethod
    def login(user, password):
        """
        Deprecated
        """
        controller = PermissionController()
        logged_user = controller.login(user, password)
=======
def create_app(config_filename):
    app = EasyRis(__name__)
    app.config.from_pyfile(config_filename)
    #print app.config
    
    from datetime import timedelta
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=app.config['PERMANENT_SESSION_LIFETIME'])
>>>>>>> Stashed changes

    # This is to prevent bad url in frontend
    app.url_map.strict_slashes = False
    
    from easyris.utils.api import cities
    from easyris.patient.api import patient
    from easyris.user.api import login_
    from easyris.examination.api.typology import typology
    from easyris.report.api import report
    from easyris.examination.api.base import examination
    
    # Register blueprint from other modules
    app.register_blueprint(patient, url_prefix='/patient')
    app.register_blueprint(cities, url_prefix='/cities')
    app.register_blueprint(typology, url_prefix='/typology')
    app.register_blueprint(examination, url_prefix='/examination')
    app.register_blueprint(login_, url_prefix='')
    app.register_blueprint(report, url_prefix="/report")
    
    from flask_debugtoolbar import DebugToolbarExtension
    app.toolbar = DebugToolbarExtension(app)
    
    from flask.ext.login import LoginManager
    app.login_manager = LoginManager()
    app.login_manager.init_app(app)
    
    
    # Database connection
    from mongoengine import connect
    db_name = app.config['DATABASE_NAME']
    # db_port = app.config['DATABASE_PORT']
    connect(db_name)
    
    #connect(
    #        name='easyris',
    #        username='user',
    #        password='12345',
    #        host='mongodb://admin:qwerty@localhost/production'
    #        )
    
    return app
    