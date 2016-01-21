from flask import Flask
from utils.api import cities
from patient.api import patient
from flask.ext.cors import CORS

app = Flask(__name__)
app.register_blueprint(patient, url_prefix='/patient')
app.register_blueprint(cities, url_prefix='/cities')
CORS(app)

@app.route('/')
def entry():
    return "Hello EasyRIS!"


if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True)
