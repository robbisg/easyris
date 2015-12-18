from model import Patient
from mongoengine import *
from datetime import datetime

# TODO: Database name should be explicit?
connect('easyris', port=27017)

class PatientController(object):
    
    def __init__(self, *args, **kwargs):
        self._currentPatient = Patient.objects().first()
    
    
    def add(self, **query):
        if 'birthdate' in query.keys():
            query['birthdate'] = datetime.strptime(query['birthdate'], 
                                                   "%Y-%m-%dT%H:%M:%S" )
        try:
            patient = Patient(**query)
            patient.save()
        except (FieldDoesNotExist, 
                KeyError,
                SaveConditionError) as err:
            return str(err)
        
        #TODO: Is it useful for the program?
        self._currentPatient = patient
        
        return "Patient correctly inserted!"
    
    
    def update(self, **query):
        
        patient = self._currentPatient
        # TODO: Include checks in function??
        if 'birthdate' in query.keys():
            query['birthdate'] = datetime.strptime(query['birthdate'], 
                                                   "%Y-%m-%dT%H:%M:%S" )
        if patient.modify(**query):
            patient.save()
            return "Correctly modified"
        
        return "Error modifying patient!"
    
    
    def search(self, **query):
        
        # TODO: Check query fields!
        patients = Patient.objects(**query)

        if patients.count() == 0:
            return 'ERR'
        else:
            # TODO: Check if patient is "Attivo"
            return patients

    
    
    def delete(self, status, note):
        #TODO: Is it useful?? Yes for me!
        return self.update(status=status, status_note=note)


    def get_patient(self, id_):
        
        self._currentPatient = self.search(id_patient=id_).first()
        return self._currentPatient