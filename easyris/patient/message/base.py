from easyris.base.message.message import MessageHeader


class PatientCorrectHeader(MessageHeader):
    
    def __init__(self, 
                 code=100, 
                 message='List of Patients present', 
                 user=None, **kwargs):
        
        MessageHeader.__init__(self, code, message, user, **kwargs)


class PatientNoRecordHeader(MessageHeader):
    
    def __init__(self, 
                 code=101, 
                 message='No Patient in database', 
                 user=None, 
                 **kwargs):
        MessageHeader.__init__(self, code, message, user, **kwargs)
        


class PatientErrorHeader(MessageHeader):
    
    def __init__(self, 
                 code=102, 
                 message='Error with Patient', 
                 user=None, 
                 **kwargs):
        MessageHeader.__init__(self, code, message, user, **kwargs)
        
        
