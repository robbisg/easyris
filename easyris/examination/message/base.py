from easyris.base.message import MessageHeader


class ExaminationErrorHeader(MessageHeader):
    
    
    def __init__(self, 
                 code=202, 
                 message='Error with Examination', 
                 user=None, 
                 **kwargs):
        MessageHeader.__init__(self, code, message, user, **kwargs)
        


class ExaminationNoRecordHeader(MessageHeader):
    
    
    def __init__(self, 
                 code=201, 
                 message='No Examination in database', 
                 user=None, 
                 **kwargs):
        MessageHeader.__init__(self, code, message, user, **kwargs)
        

class ExaminationCorrectHeader(MessageHeader):
    
    def __init__(self, 
                 code=200, 
                 message='Examination correctly loaded', 
                 user=None, **kwargs):
        
        MessageHeader.__init__(self, code, message, user, **kwargs)