from qScience.log.event import Log, Event
from mongoengine import connect
from pymongo import ReadPreference
import pdfkit
import os
import urllib2
import json
import logging
from celery import Celery

logger = logging.getLogger('easyris_logger')
celery_ = Celery('easyris_celery')


@celery_.task
def message_to_db(username, message, code):
    """
    Deprecated:
    We only use text file
    """
    
    _ = connect('easyris_log', 
                host='mongodb://192.168.50.100:27017,192.168.50.99:27017', 
                replicaSet='rs0', 
                read_preference=ReadPreference.PRIMARY_PREFERRED)
    log = Log(username=str(username),
              message=str(message),
              code=str(code))
    log.save()
    #print "Log saved!"
    return



@celery_.task
def save_event(event_dict):
    
    from qScience.database.base import parse_db_config, easyris_connect
    
    db_config = parse_db_config("config/database.cfg")
    db_config['database_name'] = 'easyris_log'
    db_client = easyris_connect(**db_config)
    
    print event_dict
    
    event = Event(**event_dict)
    event.save()
    
    return "Event saved!"



@celery_.task
def save_pdf(html, filename):
    pdfkit.from_string(html, os.path.join('/vagrant/',filename))
    print 'Save '+filename
    return


def _build_pacs_data(examination):
    
    patient_birthdate = "%s-%02d-%02d" % (examination.id_patient.birthdate.year,
                                          examination.id_patient.birthdate.month,
                                          examination.id_patient.birthdate.day)
    
    dott_first = examination.medico_richiedente.split(' ')[0]
    dott_last = examination.medico_richiedente.split(' ')[-1]
    
    #station_id = station_id_dict[examination.id_typology.station_id]
    
    data = {
            "order": {
                "accession_number":                     str(examination.id), # Passare a monte!
                "patient_id":                           str(examination.id_patient.id_patient),
                "patients_birth_date":                  patient_birthdate,
                "patients_sex":                         str(examination.id_patient.gender),
                "requested_procedure_description":      str(examination.id_typology.descrizione_breve),
                "station_id":                           "1", # str(station_id)
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

    print data
    
    return data


@celery_.task
def send_to_pacs(data):

    import ConfigParser
    import sys
    
    config_ = ConfigParser.ConfigParser()
    config_.read(os.path.join(sys.path[0], "config/pacs.cfg"))
    
    url = str(config_.get('pacs', 'url'))
    #print url.__class__
    #url="http://192.168.30.225:6000/api/v1/orders"
    headers = {'Accept': 'application/json',
               'Content-Type':'application/json'}
    
    request = urllib2.Request(url, 
                              data=json.dumps(data), 
                              headers=headers)
    
    logger.info(request.get_full_url())
    print request.get_full_url()
    logger.info(request.data)
    logger.info(request.headers)
    # Send to log?
    try:
        _ = urllib2.urlopen(request)
    except Exception,err:
        print err


@celery_.task(bind=True)
def pacs_error_handler(self, uuid):
    result = self.app.AsyncResult(uuid)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          uuid, result.result, result.traceback))