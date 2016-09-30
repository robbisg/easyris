from easyris.base.message.message import MessageHeader


class ReportCorrectHeader(MessageHeader):
    
    def __init__(self, 
                 code=500, 
                 message=None,
                 user=None, **kwargs):
        

        MessageHeader.__init__(self, code, message, user, **kwargs)




class ReportActionForbidden(MessageHeader):

    def __init__(self, 
                 code=505, 
                 message='%s forbidden',
                 action='None',
                 user=None, **kwargs):
        
        
        message = message % (action)
        MessageHeader.__init__(self, code, message, user, **kwargs)
        


class ReportErrorHeader(MessageHeader):
    
    def __init__(self, 
                 code=501, 
                 message=None,
                 user=None, **kwargs):
        

        MessageHeader.__init__(self, code, message, user, **kwargs)