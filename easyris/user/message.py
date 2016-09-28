from easyris.base.message.message import MessageHeader


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