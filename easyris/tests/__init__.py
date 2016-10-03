from numpy import random

def _get_current_patient_id(num='0001'):
    from datetime import datetime
    year = str(datetime.now()).split('-')[0]
    month = str(datetime.now()).split('-')[1]
    
    return year+month+num