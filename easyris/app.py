from flask import Flask
from patient.api import patient_app 
from flask.ext.cors import CORS

app = Flask(__name__)
app.register_blueprint(patient_app, url_prefix='/patient')
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
