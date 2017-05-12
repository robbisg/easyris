from flask import Blueprint
from flask_cors import cross_origin
from qScience.controller.cities import CityController
from qScience.utils.decorators import jsonp
from qScience.message.base.utils import build_response

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