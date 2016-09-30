from easyris.patient.controller import PatientController
from easyris.base.action import action_factory
from easyris.base.action.examination import *
from easyris.examination.controller import ExaminationController, TypologyController
from easyris.user.controller import PermissionController
from easyris.report.controller import ReportController

class Mapper(object):
    _map = dict()
    
    @classmethod
    def get_mapped(cls, name):
        return cls._map[name]



class ControllerMapper(Mapper):
    
    _map = {
            'patient': PatientController,
            'examination': ExaminationController,
            'typology': TypologyController,
            'user': PermissionController,
            'report': ReportController
            }
       
    # TODO: Method to add/remove controllers   
       

class ActionMapper(Mapper):
    
    '''
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
    '''
    
    @classmethod
    def get_mapped(cls, name):
        return action_factory(name)
