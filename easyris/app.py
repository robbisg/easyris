from flask import Flask
from utils.api import cities
from patient.api import patient
from flask.ext.cors import CORS


#import cryptography
#from OpenSSL import crypto
#from OpenSSL import SSL
#import os
#context = SSL.SSLContext(SSL.PROTOCOL_TLSv1_2)
#context.load_cert_chain('/etc/webserver-ssl/webserver.crt','/etc/webserver-ssl/webserver.key')
#cer = os.path.join(os.path.dirname(__file__), '/etc/webserver-ssl/webserver.crt')
#key = os.path.join(os.path.dirname(__file__), '/etc/webserver-ssl/webserver.key')
 

app = Flask(__name__)
app.register_blueprint(patient, url_prefix='/patient')
app.register_blueprint(cities, url_prefix='/cities')
CORS(app)

@app.route('/')
def entry():
    return "Hello EasyRIS!"


if __name__ == '__main__':
    #app.debug = True
    
#    context = ( cer, key )

    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True,
		ssl_context=('/etc/webserver-ssl/webserver.crt', '/etc/webserver-ssl/webserver.key')
 #           ssl_context=context
		)
