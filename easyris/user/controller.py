from easyris.user.model import User

class PermissionController(object):
    
    def login(self, user, password):
        
        logged_user = User.objects(username=user).first()
        
        if len(logged_user) == 0:
            # No user with this username
            print 'No user with this username'
            return None
        
        if logged_user.check_password(password):
            return logged_user
        
        return None
    
    def load_user(self, id_):
        
        return User.objects(id=id_).first()
        
            
        