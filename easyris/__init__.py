import sys, os
from flask import Flask
from easyris.user.controller import PermissionController
from mongoengine import connect


sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
__version__ = '0.0.1'


class EasyRis(Flask):
    ## Should be a Singleton??
    
    def __init__(self, import_name, static_path=None, static_url_path=None, 
        static_folder='static', template_folder='templates', 
        instance_path=None, instance_relative_config=False):
        
        # TODO: Migrate to flask-mongoengine?
        #connect('easyris', port=27017)
        
        Flask.__init__(self, 
                       import_name, 
                       static_path=static_path, 
                       static_url_path=static_url_path, 
                       static_folder=static_folder, 
                       template_folder=template_folder, 
                       instance_path=instance_path, 
                       instance_relative_config=instance_relative_config)
            
    @staticmethod
    def login(user, password):
        
        controller = PermissionController()
        logged_user = controller.login(user, password)

        if logged_user != None:
            #g.user = logged_user
            return True, logged_user
        return False, None
        
    
    def get_user(self, id_user):
        controller = PermissionController()
        return controller.load_user(id_user)
        
        