from mongoengine.document import Document
from mongoengine.fields import DateTimeField, StringField
from datetime import datetime

class Log(Document):
    
    __collection__ = 'message_log'
    
    data_log = DateTimeField(required=True, default=datetime.now())
    username = StringField(required=True)
    message = StringField(required=True)
    code = StringField(required=True)