from flask import Flask
from utils.api import cities
from patient.api import patient
from flask.ext.cors import CORS
from easyris import EasyRis

app = Flask(__name__)
system = EasyRis()
app.register_blueprint(patient, url_prefix='/patient')
app.register_blueprint(cities, url_prefix='/cities')
CORS(app)

@app.route('/')
def entry():
    user = 'roberto'
    password = 'roberto'
    system.login(user, password)
    return "Hello EasyRIS!"


if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True)
