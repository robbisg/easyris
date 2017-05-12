from qScience.message.base import MessageHeader


class UserLoggedHeader(MessageHeader):
    
    def __init__(self, 
                 code=400, 
                 message='User Logged In', 
                 user=None, **kwargs):
        
        MessageHeader.__init__(self, code, message, user, **kwargs)


class UserNotFoundHeader(MessageHeader):
    
    def __init__(self, 
                 code=401, 
                 message='User not present in the database', 
                 user=None, 
                 **kwargs):
        MessageHeader.__init__(self, code, message, user, **kwargs)
        


class UserNotAuthenticatedHeader(MessageHeader):
    
    def __init__(self, 
                 code=402, 
                 message='User not authenticated', 
                 user=None, 
                 **kwargs):
        MessageHeader.__init__(self, code, message, user, **kwargs)
        

class UserNotHavingRole(MessageHeader):
    
    def __init__(self, 
                 code=403, 
                 message='User has not role %s', 
                 user=None,
                 role='medico',
                 **kwargs):
        message = message % (role)
        MessageHeader.__init__(self, code, message, user, **kwargs)