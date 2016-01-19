from model import Patient
from mongoengine import *
from datetime import datetime

# TODO: Database name should be explicit?

connect('easyris', port=27017)


class PatientController(object):
    
    def __init__(self, *args, **kwargs):
        # TODO: If no patients??
        
        self._currentPatient = Patient.objects().first()

    
    def add(self, **query):
        
        # TODO: Check fields if they're correct!
        # TODO: Manage birthdate.
        # TODO: Check sul codice fiscale se esiste il paziente.
        
        
        if 'birthdate' in query.keys():
            query['birthdate'] = datetime.strptime(query['birthdate'], 
                                                   "%Y-%m-%dT%H:%M:%S" )
            
        patient = Patient(**query)
        try:
            patient.save()
        except (FieldDoesNotExist,
                NotUniqueError,
                SaveConditionError) as err:
            return 'ERR'
        
        #TODO: Is it useful for the program?
        self._currentPatient = patient
        
        return "OK"
    
    
    def update(self, **query):
        
        patient = self._currentPatient
        # TODO: Include checks in function??
        if 'birthdate' in query.keys():
            query['birthdate'] = datetime.strptime(query['birthdate'], 
                                                   "%Y-%m-%dT%H:%M:%S" )
        if patient.modify(**query):
            try:
                patient.save()
            except NotUniqueError, err:
                return 'ERR'
            
            return "OK"
        
        return "ERR"
    
    
    def search(self, **query):
        
        # TODO: Check query fields!
        
        patients = Patient.objects(**query)
        
        if patients.count() == 0:
            return None
        else:
            # TODO: Check if patient_app is "Attivo"
            return patients

    
    
    def delete(self, status, note):
        #TODO: Is it useful?? Yes for me!
        return self.update(status=status, status_note=note)


    def get_patient(self, id_):
        
        patient = self.search(id_patient=str(id_))
        if patient == None:
            return 'ERR'
        
        self._currentPatient = patient.first()
        return [self._currentPatient]
    
    