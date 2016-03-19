from flask import Response
from bson.json_util import dumps


def build_response(message):
    
    data = dumps([m.to_mongo() for m in message])
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    
    return response