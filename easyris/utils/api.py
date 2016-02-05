from flask import Blueprint, jsonify, request, Response

from mongoengine import *
from bson.json_util import dumps
import json

from controller import CityController
from utils.decorators import jsonp, crossdomain
from easyris.utils.response import build_response

cities = Blueprint('cities', __name__)
controller = CityController()


@cities.route('/', methods=['GET'])
@jsonp
def show_cities():
    message = controller.get_cities()
    
    if message == 'ERR':
        return "No cities"
        
    return build_response(message)