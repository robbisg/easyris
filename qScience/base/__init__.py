from qScience.database.base import QScienceQuerySet, QScienceMixin
from flask import Flask
from qScience.controller.user import PermissionController
from mongoengine import connect

class QScience(Flask):
    ## Should be a Singleton??
    
    def __init__(self, import_name, static_path=None, static_url_path=None, 
        static_folder='static', template_folder='templates', 
        instance_path=None, instance_relative_config=False):
        
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
        """
        Deprecated
        """
        controller = PermissionController()
        logged_user = controller.login(user, password)

        if logged_user != None:
            #g.user = logged_user
            return True, logged_user
        return False, None
        
    
    def get_user(self, id_user):
        # This seems good! :)
        controller = PermissionController()
        return controller.load_user(id_user)