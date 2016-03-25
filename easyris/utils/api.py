from flask import Blueprint, jsonify, request, Response

from mongoengine import *
from bson.json_util import dumps
import json
from flask_cors import cross_origin
from controller import CityController
from utils.decorators import jsonp
from easyris.base.middleware import build_response

cities = Blueprint('cities', __name__)
controller = CityController()


@cities.route('/', methods=['GET'])
@jsonp
@cross_origin(origin=None, 
             methods=['GET', 'OPTIONS'], 
             allow_headers=['X-Requested-With', 
                            'Content-Type', 
                            'Origin'],
             supports_credentials=True)
def show_cities():
    
    message = controller.get_cities()
    
    if message == 'ERR':
        return "No cities"
        
    return build_response(message)