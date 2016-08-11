from easyris.patient.controller import PatientController
from easyris.base.action import Create, Read, Update, Delete
from easyris.base.action.examination import *
from easyris.examination.controller import ExaminationController, TypologyController

class Mapper(object):
    _map = dict()
    
    @classmethod
    def get_mapped(cls, name):
        return cls._map[name]()



class ControllerMapper(Mapper):
    
    _map = {
            'patient': PatientController,
            'examination': ExaminationController,
            'typology': TypologyController,
            }
       
    # TODO: Method to add/remove controllers   
       

class ActionMapper(Mapper):
    
    _map = {
            'create': Create,
            'read':   Read,
            'update': Update,
            'delete': Delete,
            'start': Start,
            'go': Go,
            'stop': Stop,
            'pause': Pause,
            'finish': Finish,
            'eject': Eject,
            }
    
    # TODO: Method to add/remove actions