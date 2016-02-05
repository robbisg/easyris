import sys, os
from easyris.base.factory import ControllerMapper, ActionMapper

sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path


__version__ = '0.0.1'


class EasyRis(object):
    ## Should be a Singleton??
    
    def __init__(self):
        self.currentUser = None
    
    def do(self, action_name, resource_name, **kwargs):
        # action_name is a string
        # resource_name is a string
        
        # Check if someone is logged
        
        if self.currentUser.has_permission(action_name, resource_name):
            controller = ControllerMapper.get_mapped(resource_name)
            action = ActionMapper.get_mapped(action_name)
            return action.execute(controller, **kwargs)
        else:
            return 'Permission denied!'
            
    
    def login(self, user, password):
        
        self.currentUser = user