from easyris.base.message.message import Message
from flask import Response
from bson.json_util import dumps


def message_to_http(message):
    
    response = Response(response=message.to_json(),
                        status=200,
                        mimetype="application/json")
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
        
        