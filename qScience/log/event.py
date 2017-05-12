from mongoengine.document import Document
from mongoengine.fields import DateTimeField, StringField
from datetime import datetime

class Log(Document):
    
    __collection__ = 'message_log'
    
    data_log = DateTimeField(required=True, default=datetime.now())
    username = StringField(required=True)
    message = StringField(required=True)
    code = StringField(required=True)
    
    
class Event(Document):
    
    __collection__ = 'event_log'
    
    data_log = DateTimeField(required=True, default=datetime.now())
    username = StringField(required=True)
    page = StringField(required=True)
    element = StringField(required=True)
    event_type = StringField(required=True)
    ip = StringField(required=True)
    user_agent = StringField(required=True)