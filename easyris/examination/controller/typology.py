from easyris.examination.model import Typology
from easyris.base.message import MessageHeader, Message


# TODO: Is it possible to use a single controller
# TODO: Is it a factory?
class TypologyController(object):
    
    def __init__(self, name='typology', **kwargs):
        self.name = name
    
    
    def read(self, **query):
                
        typology = Typology.objects(**query)

        if typology.count() == 0:
            header = MessageHeader(312, 
                                   "No Typologies in the database",
                                   user=None)
            message = Message(header,
                              data=typology)
            return message
        
        header = MessageHeader(310, 
                               "List of typologies",
                               user=None)
        message = Message(header,
                          data=typology)
        return message
