from flask import Blueprint, jsonify, request, Response

from mongoengine import *
from bson.json_util import dumps
import json

from controller import CityController
from utils.decorators import jsonp, crossdomain

cities = Blueprint('cities', __name__)
controller = CityController()


@cities.route('/', methods=['GET'])
@jsonp
def show_cities():
    message = controller.get_cities()
    print message
    if message == 'ERR':
        return "No cities"
    
    data = dumps([m.to_mongo() for m in message])
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    
    return response