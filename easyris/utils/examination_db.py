from easyris.user.model import User, Permission, Role
from easyris.patient.model import Patient
from easyris.examination.model import Examination, Priority, Typology
from mongoengine import connect
import itertools
import random
from datetime import datetime

def run(database, port, n_loaded=50):
    
    client = connect(database, port=port)
    
    Examination.drop_collection()
    
    priority_list = Priority.objects()
    typology_list = Typology.objects()
    patient_list = Patient.objects()
    
    user1 = User.objects(username='gaetano').first()  
    
    for _ in range(n_loaded):
        
        ip = random.randint(0, len(patient_list)-1)
        it = random.randint(0, len(typology_list)-1)
        ipr= random.randint(0, len(priority_list)-1)

        
        patient = patient_list[ip]
        typology = typology_list[it]
        priority = priority_list[ipr]
        
        if random.randint(1, 10) > 5:
            now = datetime.now()
            date_ = datetime(year=now.year,
                             month=now.month,
                             day=now.day)
        else:
            date_ = datetime(year=2016,
                             month=02,
                             day=02)
    
        examination = Examination(id_patient=patient,
                         medico_richiedente='Mauro Caffarini',
                         data_inserimento=date_,
                         id_priority=priority,
                         id_typology=typology,
                         id_creator=user1,
                         #id_technician=user2,
                         #accession_number='12345665',
                         codice_esenzione='67577568',
                         examination_note='ok'
                         )
        
        examination.save()
        