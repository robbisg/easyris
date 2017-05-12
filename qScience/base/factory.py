from qScience.controller.patient import PatientController
from qScience.base.action import action_factory
from qScience.base.action.examination import *
from qScience.controller.examination import ExaminationController
from qScience.controller.examination_type import TypologyController
from qScience.controller.user import PermissionController
from qScience.controller.report import ReportController

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
        
    @classmethod
    def get_mapped(cls, name):
        return action_factory(name)
