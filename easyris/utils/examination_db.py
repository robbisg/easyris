from easyris.user.model import User, Permission, Role
from easyris.patient.model import Patient
from easyris.examination.model import Examination, Priority, Typology
from easyris.base.database import parse_db_config, easyris_connect
from mongoengine import connect
import itertools
import random
from datetime import datetime
from easyris.examination.status import CompletedExaminationStatus,\
    NewExaminationStatus

def run(database_config, n_loaded=50):
    
    db_config = parse_db_config(database_config)
    _ = easyris_connect(**db_config)
    #client = connect(database, port=port)
    
    Examination.drop_collection()
    
    priority_list = Priority.objects()
    typology_list = Typology.objects()
    patient_list = Patient.objects()
    
    user1 = User.objects(username='gaetano').first()
    user2 = User.objects(username='daniele').first()
    
    for _ in range(n_loaded):
        
        ip = random.randint(0, len(patient_list)-1)
        it = random.randint(0, len(typology_list)-1)
        ipr= random.randint(0, len(priority_list)-1)

        patient = patient_list[ip]
        typology = typology_list[it]
        priority = priority_list[ipr]
        
        random_number = random.randint(1, 10)
        
        if random_number > 5:
            now = datetime.now()
            date_ = datetime(year=now.year,
                             month=now.month,
                             day=now.day)
            if random_number == 8:
                status_name = 'completed'
                status = CompletedExaminationStatus()
            else:
                status_name = 'new'
                status = NewExaminationStatus()
            
        else:
            date_ = datetime(year=2016,
                             month=02,
                             day=02)
            status_name = 'completed'
            status = CompletedExaminationStatus()
    
    
        examination = Examination(id_patient=patient,
                         medico_richiedente='Mauro Caffarini',
                         data_inserimento=date_,
                         id_priority=priority,
                         id_typology=typology,
                         id_technician=user2,
                         id_creator=user1,
                         status_name=status_name,
                         status=status,
                         codice_esenzione='67577568',
                         examination_note='ok'
                         )
        
        examination.save()
        