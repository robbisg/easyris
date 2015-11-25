from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *
from pymongo import *
from codicefiscale import build


class Patient(Document):
    config_collection_name = 'patients'

    # Setting the possible values by using fields
    id_patient =StringField(required=True)
    last_name = StringField(required=True)
    gender = EnumField(StringField(), 'M', 'F',required=True)
    first_name = StringField(required=True)
    birthdate = DateTimeField(required=True)
    birthplace = StringField(required=True)
    cf_code = StringField(required=True)
    last_name_parents =  StringField(required=False)
    name_parents = StringField(required=False)
    address = StringField(required=False)
    city = StringField(required=False)
    province = StringField(required=False)
    CAP = IntField()
    phone_number = StringField(required=True)
    email = StringField(required=False)
    note = StringField(required=False)

    @computed_field
    def age(obj):
     return ((datetime.now() - birthdate).days) / 365

    def cf_code2(obj):
     return build(last_name, first_name, birthdate, gender, 'G482')

me = Patient(id_patient='1234',first_name='Piero', last_name='Chiacchiaretta',
birthdate=datetime(year=1979, day=27, month=9), birthplace='Pescara', cf_code='CHCPRI79P27G482U',
gender="M", address='Via Aldo Moro, 114', city='San Giovanni Teatino', province='Chieti',
CAP=66020, phone_number='3294946261', email='piero.chiacchiaretta@gmail.com')


# This connections to the DB and starts the session
session = Session.connect('easyris')
session.clear_collection(Patient) # clear previous runs of this code!
# Insert on a session will infer the correct collection and push the object
# into the database
session.save(me)
