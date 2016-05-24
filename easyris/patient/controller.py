from model import Patient
#from easyris.base.controller import Controller
from mongoengine import *
from datetime import datetime
from easyris.base.message.message import Message
from easyris.base.message.patient import PatientCorrectHeader, \
                                        PatientErrorHeader, \
                                        PatientNoRecordHeader
from numpy.f2py.crackfortran import get_usedict

# TODO: Database name should be explicit?

#connect('easyris', port=27017)


class PatientController(object):
        
    #name = StringField(required=True, default='patient')
    
    def __init__(self, name='patient', *args, **kwargs):
        
        # TODO: If no patients??
        self._currentPatient = None
        self.name = name
        self.user = None
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
            
            message = Message(PatientErrorHeader(message=err.message))
            
            return message
        
        # TODO: Is it useful for the program?
        self._currentPatient = patient
        
        # TODO: To be improved!
        patient = self.get_patient(patient.id_patient)
        
        message = Message(PatientCorrectHeader(),
                              data=patient)
        return message
    
    
    def update(self, **query):
        
        # Check if a patient has been selected
        print self._currentPatient
        if self._currentPatient == None:
            # Get the id from query
            if 'id_patient' in query.keys():
                _ = self.get_patient(query['id_patient'])
            
        
        patient = self._currentPatient
        
        # TODO: Include checks in function??
        if 'birthdate' in query.keys():
            query['birthdate'] = datetime.strptime(query['birthdate'], 
                                                   "%Y-%m-%dT%H:%M:%S.%fZ" )
        
        # Try to modify
        if not patient.modify(**query):
            message = Message(PatientErrorHeader(message='Error in modifying'))
            return message
        
        # Try to save
        try:
            patient.save()
        except NotUniqueError, err:
            message = Message(PatientErrorHeader(message=err.message, 
                                                     user=self.user)) 
            return message
        
        patient = self.get_patient(patient.id_patient)
        # Everything ok!!!
        message = Message(PatientCorrectHeader(),
                          data=patient)
        return message
    
    
    def read(self, **query):
        
        # TODO: Check query fields!
        
        if 'id_patient' in query.keys():
            query['id_patient'] = str(query['id_patient'])
        
        patients = Patient.objects(**query)
        print patients
        
        # Patient list empty
        if patients.count() == 0:
            message = Message(PatientNoRecordHeader(),
                              data=patients)
            return message
        
        
        # TODO: Check if patient_app is "Attivo"
        message = Message(PatientCorrectHeader(),
                          data=patients)
        return message

    
    
    def delete(self, status, note):
        # TODO: Is it useful?? Yes for me!
        return self.update(status=status, status_note=note)
        


    def get_patient(self, id_):

        patient = Patient.objects(id_patient=str(id_))
        
        #TODO: Is there a more elegant way to deal with that?
        if patient == None:
            return 'ERR'
        
        self._currentPatient = patient.first()
        return patient
    

    