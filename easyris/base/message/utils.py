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