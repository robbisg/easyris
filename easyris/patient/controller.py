from model import Patient
#from easyris.base.controller import Controller
from mongoengine import *
from datetime import datetime

# TODO: Database name should be explicit?

#connect('easyris', port=27017)


class PatientController(object):
        
    #name = StringField(required=True, default='patient')
    
    def __init__(self, name='patient', *args, **kwargs):
        
        # TODO: If no patients??
        self._currentPatient = None
        self.name = name
        #super(PatientController, self).__init__()
        
    def create(self, **query):
        
        # TODO: Check fields if they're correct!
        # TODO: Check sul codice fiscale se esiste il paziente.
        
        
        if 'birthdate' in query.keys():
            query['birthdate'] = datetime.strptime(query['birthdate'], 
                                                   "%Y-%m-%dT%H:%M:%S.%fZ" )
            
        patient = Patient(**query)
        try:
            patient.save()
        except (FieldDoesNotExist,
                NotUniqueError,
                SaveConditionError) as err:
            
        # TODO: Separate each error!
            return 'ERR'
        
        #TODO: Is it useful for the program?
        self._currentPatient = patient
        
        # TODO: Return message class in dict form.
        return "OK"
    
    
    def update(self, **query):
        
        if self._currentPatient == None:
            if 'id_patient' in query.keys():
                patient = self.get_patient(query['id_patient'])[0]                
        else:
            patient = self._currentPatient
        # TODO: Include checks in function??
        if 'birthdate' in query.keys():
            query['birthdate'] = datetime.strptime(query['birthdate'], 
                                                   "%Y-%m-%dT%H:%M:%S.%fZ" )
        if patient.modify(**query):
            try:
                patient.save()
            except NotUniqueError, err:
                return 'ERR'
            
            return "OK"
        
        return "ERR"
    
    
    def read(self, **query):
        
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
        
        patient = self.read(id_patient=str(id_))
        if patient == None:
            return 'ERR'
        
        self._currentPatient = patient.first()
        return [self._currentPatient]
    
    