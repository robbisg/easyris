from easyris.examination.model import Examination
from collections import Counter
from datetime import datetime

def _get_correct_examinations():
    examination_list = Examination.objects(status_name='completed',
                                           data_inserimento=datetime(2016, 2, 2, 0, 0))
    patient_id = [e.id_patient.id for e in examination_list]
    counter = Counter(patient_id)
    items_ = counter.elements()
        
    c = items_.next()
    
    while counter[c] <= 2:
        c = items_.next()

    
    return Examination.objects(id_patient=c,
                               data_inserimento=datetime(2016, 2, 2, 0, 0),
                               status_name='completed')
    
    
def _get_random_examinations():
    return Examination.objects[:5]
    
    