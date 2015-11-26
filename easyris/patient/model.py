from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *
from pymongo import *
from codicefiscale import build
from code_comuni import CF_codici_comuni

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
    age = IntField()
    cf_calc = StringField(required=True)
    nationality = StringField(required=True)

    @property
    def age_calc(self):
     return ((datetime.now() - self.birthdate).days) / 365

    @property
    def cf_code_calc(self):

        client = MongoClient()
        db = client.easyris

        result=db.get_collection('CF_codici_comuni').find({'Denom_Italiana' :self.birthplace})
        result2=result.next()
        cf_code=result2['Codice']
        return build(self.last_name, self.first_name, self.birthdate, self.gender, str(cf_code))


# me = Patient(id_patient='1234',first_name='Piero', last_name='Chiacchiaretta',
# birthdate=datetime(year=1979, day=27, month=9), birthplace='AGRIGENTO', cf_code='CHCPRI79P27G482U',
# gender="M", address='Via Aldo Moro, 114', city='San Giovanni Teatino', province='Chieti',
# CAP=66020, phone_number='3294946261', email='piero.chiacchiaretta@gmail.com', nationality='italiana')
#
#
# me = Patient(id_patient='1234',first_name='Piero', last_name='Chiacchiaretta',
# birthdate=datetime(year=1979, day=27, month=9), birthplace='AGRIGENTO', cf_code='CHCPRI79P27G482U',
# gender="M", address='Via Aldo Moro, 114', city='San Giovanni Teatino', province='Chieti',
# CAP=66020, phone_number='3294946261', email='piero.chiacchiaretta@gmail.com', nationality='italiana',
# age= me.age_calc, cf_calc=me.cf_code_calc)
#
#
# # This connections to the DB and starts the session
# session = Session.connect('easyris')
# session.clear_collection(Patient) # clear previous runs of this code!
# # Insert on a session will infer the correct collection and push the object
# # into the database
# session.save(me)
