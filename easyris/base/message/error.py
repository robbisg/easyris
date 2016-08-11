from message import MessageHeader


class NotFoundHeader(MessageHeader):
    
        def __init__(self,
                     name,
                     code=001, 
                     message='%s not found in the database', 
                     user=None, **kwargs):
        
            MessageHeader.__init__(self, code, message % (name), user, **kwargs)
            

class NotImplementedApiHeader(MessageHeader):
    
        def __init__(self, 
                     code=002, 
                     message='Endpoint not implemented', 
                     user=None, **kwargs):
            
            MessageHeader.__init__(self, code, message, user, **kwargs)