import json
from bson.json_util import dumps

class MessageHeader(object):
       
    # TODO: Store message in database. Avoid duplicate code.
    def __init__(self, code, message, user, **kwargs):
        
        self._allowed_optional_headers = self.set_allowed_headers()
        self.code = code
        self.message = message
        self.user = user
        
        self._field = ['code', 'user', 'message']
        
        # This is intended to be an extension of header
        # using a dictionary we could add several field
        for arg in kwargs:
            if (arg in self._allowed_optional_headers) or \
                ('*' in self._allowed_optional_headers):
                setattr(self, arg, kwargs[arg])
                self._field.append(arg)
    
    
    def set_allowed_headers(self, key_list=['*']):
        
        self._allowed_optional_headers = key_list
        return
    
    def set_user(self, user):
        self.user = user


class BadClassMessageHeader(MessageHeader):
    
    def __init__(self, user, **kwargs):
        
        # TODO: Code and messages are completely random
        code = 1
        message = 'The message header is not good!'
        MessageHeader.__init__(self, code, message, user, **kwargs)


class Message(object):
    
    def __init__(self, header, data=None):
        
        # Check if header is a real Header!
        
        if not isinstance(header, MessageHeader):
            header = BadClassMessageHeader(user='system')
            print 'oh'
            data = None
        
        self.header = header
        
        self.data = data
        self.to_db()


    def to_json(self):
        json_ = dict()
        
        for f in self.header._field:
            json_[f] = getattr(self.header, f)
        
        if self.data != None:
            json_['data'] = self.data.as_pymongo()
            
        return dumps([json_])
    
    def to_db(self):
        # TODO: Implement it!
        # TODO: Asynchronous celery task to mongo
        return None
    
    
    def set_user(self, user):
        self.header.set_user(user)
        

def message_factory(header, data):
    return Message(header=header, data=data)
        
        