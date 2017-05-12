from qScience.message.base import Message
from flask import Response
from bson.json_util import dumps
import logging


logger = logging.getLogger('easyris_logger')


def message_to_http(message):
    
    response = Response(response=message.to_json(),
                        status=200,
                        mimetype="application/json")
    
    logger.info("User "+str(message.header.user)+" - "+str(message.header.message))
    
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
        
