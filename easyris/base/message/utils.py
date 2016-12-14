from easyris.base.message.message import Message
from easyris.base.async import message_to_db
from flask import Response
from bson.json_util import dumps
import logging


logger = logging.getLogger('easyris_logger')


def message_to_http(message):
    
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
        
