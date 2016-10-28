from easyris.base.message.message import Message
from easyris.base.message.log import Log
from flask import Response, current_app
from bson.json_util import dumps
import logging
from celery import Celery
from mongoengine import connect
import pdfkit
import os

logger = logging.getLogger('easyris_logger')
celery_ = Celery('easyris_celery')


def message_to_http(message):
    
    message.to_db()
    response = Response(response=message.to_json(),
                        status=200,
                        mimetype="application/json")
    
    logger.debug("User "+str(message.header.user)+"\n"+str(message.header.message))
    
    message_to_db.delay(username=message.header.user, 
                        message=message.header.message, 
                        code=message.header.code)
    return response



def build_response(message):
    
    data = dumps([m._to_easyris() for m in message])
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    
    return response


def build_http_response(message):
    
    if not isinstance(message, Message):
        message = Message(1, "Bad Message Compose")
        
@celery_.task
def message_to_db(username, message, code):
    
    _ = connect('easyris_log')
    log = Log(username=str(username),
              message=str(message),
              code=str(code))
    log.save()
    #print "Log saved!"
    return


@celery_.task
def save_pdf(html, filename):
    pdfkit.from_string(html, os.path.join('/home/vagrant/',filename))
    print 'Save '+filename
    return


def _build_pacs_data(examination):
    
    patient_birthdate = "%s-%02d-%02d" % (examination.id_patient.birthdate.year,
                                          examination.id_patient.birthdate.month,
                                          examination.id_patient.birthdate.day)
    
    dott_first = examination.medico_richiedente.split(' ')[0]
    dott_last = examination.medico_richiedente.split(' ')[-1]
    
    data = {
            "order": {
                "patient_id":                           str(examination.id_patient.id_patient),
                "patients_birth_date":                  patient_birthdate,
                "patients_sex":                         str(examination.id_patient.gender),
                "requested_procedure_description":      str(examination.id_typology.descrizione_breve),
                "station_id":                           "1", # Per adesso 3 poi si vedra
                "patients_weight":                      "80", # Non ce l'abbiamo
                "patients_name_attributes": {
                    "family":                           str(examination.id_patient.last_name),
                    "given":                            str(examination.id_patient.first_name),
                    "middle":                           "",
                    "prefix":                           "",
                    "suffix":                           ""
                                            },
                "referring_physicians_name_attributes": {
                      "family":                         dott_last,
                      "given":                          dott_first,
                      "prefix":                         "Dr."
                                                        }
                      }
            }
    
    return data


def send_to_pacs(examination):
    
    import urllib2
    import json
    
    # from file
    url = "http://localhost:6000//api/v1/orders"
    headers = {'Accept': 'application/json','Content-Type':'application/json'}
    data = _build_pacs_data(examination)
    
    request = urllib2.Request(url, data=json.dumps(data), headers=headers)
    logger.debug(request.get_full_url())
    logger.debug(request.data)
    logger.debug(request.headers)
    # Send to log?
    try:
        _ = urllib2.urlopen(request)
    except Exception, err:
        print err
    
    return 
    