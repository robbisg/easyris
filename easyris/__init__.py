import sys, os
sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path


__version__ = '0.0.1'


class EasyRis(object):
    
    def __init__(self, user):
        self.currentUser = user
        
    def do(self, action, resource, **kwargs):
        if self.currentUser.has_permission(action, resource):
            return action.execute(resource, **kwargs)
        else:
            return 'Permission denied!'
            
    
    def login(self, user, password):
        
        self.currentUser = user