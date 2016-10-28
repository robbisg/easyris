from easyris.user.model import User
from easyris.base.message import Message
from easyris.user.message import UserLoggedHeader, \
    UserNotAuthenticatedHeader, UserNotFoundHeader
import logging


logger = logging.getLogger('easyris_logger')

class PermissionController(object):
    
    def __init__(self, name='permission', user=None):
        self.name = name
        self.user = user
        return
    
    
    def login(self, username=None, password=None):
        
        message_data = {'is_authenticated':False,
                        'user':None,
                        'qs':None}
        qs = User.objects(username=username)

        logged_user = qs.first()
        
        if len(qs) == 0:
            # No user with this username
            message = Message(UserNotFoundHeader(), 
                              data=message_data)
            logger.debug(message.header.message)
            return message

        
        if logged_user.check_password(password):
            message_data['user'] = logged_user
            message_data['is_authenticated'] = True
            message_data['qs'] = qs
            message = Message(UserLoggedHeader(), 
                              data=message_data)
            logger.debug(message.header.message)
        else:
            message = Message(UserNotAuthenticatedHeader(), 
                              data=message_data)
            logger.debug(message.header.message)
        
        return message
    
    
    def logout(self, **query):
        return Message(UserLoggedHeader(message='User logged out!'), 
                              data=None)
    
    
    
    def load_user(self, id_):
        return User.objects(id=id_).first()
    
    
       
            
        