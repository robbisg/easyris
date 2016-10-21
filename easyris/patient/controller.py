from model import Patient
#from easyris.base.controller import Controller
from mongoengine import *
from datetime import datetime
from easyris.base.message.message import Message
from easyris.patient.message import PatientCorrectHeader, \
                                        PatientErrorHeader, \
                                        PatientNoRecordHeader
from easyris.utils import parse_date
import logging


logger = logging.getLogger('easyris_logger')


class PatientController(object):
        
    
    def __init__(self, name='patient', user=None, **kwargs):
        
        # TODO: If no patients??
        self._currentPatient = None
        self.name = name
        self.user = user
        #super(PatientController, self).__init__()
        
    def create(self, **query):
        
        # TODO: Check fields if they're correct!
        
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
            logger.error(err.message)
            
            return message
        
        patient = self._get_patient(patient.id_patient)
        self._currentPatient = patient.first()
        
        message = Message(PatientCorrectHeader(message='Patient correctly created!'),
                              data=patient)

        return message
    
    
    def update(self, **query):
        
        # Check if a patient has been selected
        if self._currentPatient == None:
            # Get the id from query
            if 'id_patient' in query.keys():
                _ = self._get_patient(str(query['id_patient']))
        
        patient = self._currentPatient
        
        if 'birthdate' in query.keys():
            query['birthdate'] = parse_date(query['birthdate'])
            logger.debug(query['birthdate'])
            
        if '_id' in query.keys():
            _ = query.pop('_id')
        
        # Try to modify
        if not patient.modify(**query):
            message = Message(PatientErrorHeader(message='Error in modifying'))
            logger.error(message.header.message)
            return message
        
        # Try to save
        try:
            patient.save()
        except NotUniqueError, err:
            message = Message(PatientErrorHeader(message=err.message, 
                                                     user=self.user)) 
            logger.error(message.header.message)
            return message
        
        patient = self._get_patient(patient.id_patient)
        
        # Everything ok!!!
        message = Message(PatientCorrectHeader(message='Patient correctly modified!'),
                          data=patient)
        
        return message
    
    
    def read(self, **query):
        
        # TODO: Check query fields!
        
        if 'id_patient' in query.keys():
            query['id_patient'] = str(query['id_patient'])
        
        # return only present patients!
        query['status'] = 'Attivo'
        
        patients = Patient.objects(**query)
        
        # Patient list empty
        if patients.count() == 0:
            message = Message(PatientNoRecordHeader(),
                              data=patients)
            logger.error(message.header.message)
            return message
        
        message = Message(PatientCorrectHeader(),
                          data=patients)
        
        return message

    
    def delete(self, status, note):
        return self.update(status=status, status_note=note)
        

    def _get_patient(self, id_):
        """Deprecated"""
        patient = Patient.objects(id_patient=str(id_))
        
        #TODO: Is there a more elegant way to deal with that?
        if len(patient) == 0:
            logger.error('No Patient in the database')
            return 'ERR'
        
        self._currentPatient = patient.first()
        return patient
    
    