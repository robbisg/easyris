from flask import Response
from bson.json_util import dumps
import json



class Message(object):
    
    def __init__(self, code, message, data=None):
        
        self.code = code
        self.message = message
        self.data = data

    def to_json(self):
        
        return json.dumps(self.__dict__)
    
        
def build_message(code, message, data=None):
    
    m = Message(code, message, data=data)
    return m


def build_response(message):
    
    data = dumps([m.to_mongo() for m in message])
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    
    return response