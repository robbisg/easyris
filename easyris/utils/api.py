from flask import Blueprint, jsonify, request, Response

from mongoengine import *
from bson.json_util import dumps
import json

from controller import CityController
from utils.decorators import jsonp, crossdomain
from easyris.base.middleware import build_response

cities = Blueprint('cities', __name__)
controller = CityController()


@cities.route('/', methods=['GET'])
@jsonp
@crossdomain(origin='*', 
             methods=['GET'], 
             headers=['X-Requested-With', 
                      'Content-Type', 
                      'Origin'])
def show_cities():
    
    message = controller.get_cities()
    
    if message == 'ERR':
        return "No cities"
        
    return build_response(message)