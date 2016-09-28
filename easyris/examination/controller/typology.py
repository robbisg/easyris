from easyris.examination.model import Typology
from easyris.base.message import MessageHeader, Message


# TODO: Is it possible to use a single controller
# TODO: Is it a factory?

import logging
logger = logging.getLogger("easyris_logger")


class TypologyController(object):
    
    def __init__(self, name='typology', user=None, **kwargs):
        self.name = name
        self.user = user
    
    
    def read(self, **query):
                
        typology = Typology.objects(**query)

        if typology.count() == 0:
            header = MessageHeader(312, 
                                   "No Typologies in the database",
                                   user=None)
            message = Message(header,
                              data=typology)
            
            logger.error(message.header.message)
            return message
        
        header = MessageHeader(310, 
                               "List of typologies",
                               user=None)
        message = Message(header,
                          data=typology)
        logger.debug(message.header.message)
        return message
