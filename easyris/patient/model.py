from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *

class Patient(Document):
    config_collection_name = 'patients'

    # Setting the possible values by using fields
    id_patient = StringField()
    last_name = StringField()
    first_name = StringField()
    birthdate = StringField()
    birthplace = StringField()
    cf_code = StringField()
    last_name_parents =  StringField(required=False)
    name_parents = StringField(required=False)
    address = StringField()
    city = StringField()
    province = StringField()
    CAP = StringField()
    phone_number = StringField()
    email = StringField()
    note = StringField()

me = Patient(id_patient='1234',first_name='Piero', last_name='Chiacchiaretta',
            birthdate='27/09/1979', birthplace='Pescara', cf_code='CHCPRI79P27G482U',
            address='Via Aldo Moro, 114', city='San Giovanni Teatino', province='Chieti',
            CAP='66020', phone_number='3294946261', email='piero.chiacchiaretta@gmail.com',
            )


# This connections to the DB and starts the session
session = Session.connect('easyris')
session.clear_collection(Patient) # clear previous runs of this code!
# Insert on a session will infer the correct collection and push the object
# into the database
session.save(me)
