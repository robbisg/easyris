from qScience.model.cities import City
from mongoengine import *
from datetime import datetime


class CityController(object):
    
    def get_cities(self):
        
        cities = City.objects.only("Denom_Italiana")
        
        if cities.count() == 0:
            return None
        else:
            return cities