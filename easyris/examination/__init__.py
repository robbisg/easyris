from easyris.examination.model import Examination
from collections import Counter

def _get_correct_examinations():
    examination_list = Examination.objects(status_name='completed')
    patient_id = [e.id_patient.id for e in examination_list]
    counter = Counter(patient_id)
    items_ = counter.elements()
        
    c = items_.next()
    
    while counter[c] <= 2:
        c = items_.next()

    
    return Examination.objects(id_patient=c,
                               status_name='completed')
    
    
def _get_random_examinations():
    return Examination.objects[:5]
    
    