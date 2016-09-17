
def _get_current_patient_id():
    from datetime import datetime
    year = str(datetime.now()).split('-')[0]
    month = str(datetime.now()).split('-')[1]
    
    return year+month+'0001'