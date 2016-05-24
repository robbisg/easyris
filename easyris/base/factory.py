from easyris.patient.controller import PatientController
from easyris.base.action import Create, Read, Update, Delete


class Mapper(object):
    _map = dict()
    
    @classmethod
    def get_mapped(cls, name):
        return cls._map[name]



class ControllerMapper(Mapper):
    
    _map = {
            'patient': PatientController
            }
       
    # TODO: Method to add/remove controllers   
       

class ActionMapper(Mapper):
    
    _map = {
            'create': Create,
            'read':   Read,
            'update': Update,
            'delete': Delete,
            }
    
    # TODO: Method to add/remove actions