from flask import Flask
from utils.api import cities
from patient.api import patient
from flask.ext.cors import CORS
from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user
from easyris import EasyRis

app = Flask(__name__)

# Register blueprint from other modules
app.register_blueprint(patient, url_prefix='/patient')
app.register_blueprint(cities, url_prefix='/cities')

CORS(app)
# Login manager extensions
login_manager = LoginManager(app)

system = EasyRis()


@app.route('/')
def entry():
    return "Hello EasyRIS!"
'''
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
'''
if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True)
