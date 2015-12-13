from mongoengine import *
from pymongo import MongoClient
from codicefiscale import build
from utils.code_comuni import CF_codici_comuni
from datetime import datetime

GENDER = (('M', 'Male'),
        ('F', 'Female'))
STATUS = ('Attivo', 'Revocato', 'Defunto')

class Patient(Document):
    __collection__ = 'patients'
    
    # Setting the possible values by using fields
    id_patient = StringField(required=True, unique=True)
    
    last_name = StringField(required=True)
    first_name = StringField(required=True)
    
    gender = StringField(max_length=1, 
                         required=True, 
                         choices=GENDER)
    
    birthdate = DateTimeField(required=True)
    birthplace = StringField(required=True)
    
    codice_fiscale = StringField(required=True)
    
    last_name_parents =  StringField(required=False)
    name_parents = StringField(required=False)
    
    address = StringField(required=False)
    city = StringField(required=False)
    province = StringField(required=False, max_length=2)
    cap = StringField(required=True)
    phone_number = StringField(required=True)
    email = StringField(required=False)
    note = StringField(required=False)
    age = IntField()

    nationality = StringField(required=True)

    patient_status = StringField(required=False, choices=STATUS)
    patient_status_note = StringField(required=False)
    
        
    def clean(self):        
        
        self.compute_age()
        self.compute_cf()
        self.compute_id()
    
    
    def compute_age(self):
        self.age = ((datetime.now() - self.birthdate).days) / 365


    def compute_cf(self):
        
        client = MongoClient()
        db = client.easyris
        query=db.get_collection('CF_codici_comuni').find({'Denom_Italiana' :self.birthplace})
        result=query.next()
        cf_code=result['Codice']
        self.codice_fiscale = build(self.last_name, 
                                    self.first_name, 
                                    self.birthdate, 
                                    self.gender, 
                                    str(cf_code))
        self.province = result['Prov']


    def compute_id(self):

        n_collection = Patient.objects.count()           
        print n_collection
        id_count=str(n_collection+1).zfill(4)
        year = str(datetime.now()).split('-')[0]
        month = str(datetime.now()).split('-')[1]
        
        id_calc = year+month+id_count
        print id_calc
        self.id_patient = id_calc

