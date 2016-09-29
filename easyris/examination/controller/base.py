from easyris.examination.model import Typology, Examination, Priority
from easyris.examination.message import ExaminationCorrectHeader, ExaminationErrorHeader, \
                                        ExaminationNoRecordHeader
from easyris.examination.status import NewExaminationStatus
from easyris.patient.controller import PatientController
from easyris.base.message.message import Message
from easyris.base.message.error import NotFoundHeader
from easyris.user.model import User
from datetime import datetime
from easyris.utils import parse_date
from mongoengine import *
import logging

logger = logging.getLogger('easyris_logger')

class ExaminationController(object):
    
    def __init__(self, name='examination', user=None):
        self._currentExamination = None
        self.name = name
        self.user = user
        return
    
    def _get_examination(self, id_examination):
        """Deprecated"""
        examination = Examination.objects(id=str(id_examination))
        
        if examination == None:
            logger.error("No examination in the database")
            return 'ERR'
        
        self._currentExamination = examination.first()
        return examination
    
    
    def _check_fields(self, query, **kwargs):
        
        for k_ in kwargs.keys():
            if kwargs[k_] == None:
                msg = Message(NotFoundHeader(name=k_))
                logger.error(msg.header.message)
                return msg
            else:
                if k_ == 'id_technician':
                    if not kwargs[k_].has_role('tecnico'):
                        # TODO: Ad-hoc header
                        msg = Message(NotFoundHeader(name=k_))
                        logger.error(msg.header.message)
                        return msg
                    
                query[k_] = kwargs[k_]
                
        return query
    
    
    def _get_patient(self, id):
        pt_controller = PatientController()
        pt_message = pt_controller.read(id_patient=id)
        
        if pt_message.header.code == 101:
            logger.error(pt_message.header.message)
            return pt_message
        
        return pt_message.data[0]
    
    
    def create(self, **query):
        
        pt_controller = PatientController()
        pt_message = pt_controller.read(id_patient=query['id_patient'])
        
        if pt_message.header.code == 101:
            return pt_message
        
        query['id_patient'] = pt_message.data[0]
        logger.debug(pt_message.data[0].first_name)
        
        if 'data_inserimento' in query.keys():
            query['data_inserimento'] = parse_date(query['data_inserimento'])

        query['id_creator'] = User.objects(username=query['id_creator']).first()
        
        list_examination = query.pop('exams')
        
        if len(list_examination) == 0:
            message = Message(ExaminationErrorHeader(message='No Examination in Request'))
            logger.error(message.header.message)
            return message
        
        examination = None
        
        for i, exam_ in enumerate(list_examination):
            
            typology = Typology.objects(examination_name=exam_['nome']).first()
            priority = Priority.objects(priority_name=exam_['priority']).first()
            query = self._check_fields(query,
                                   id_priority=priority,
                                   id_typology=typology,
                                   )

            if not isinstance(query, dict):
                # It is a message!
                return query
            
            qs = Examination.objects(**query)
            
            logger.debug(query)
            logger.debug("No. of examinations: "+str(len(qs)))
            
            if len(qs) != 0:
                continue
            
            examination = Examination(**query)
        
            try:
                examination.save()
            except (FieldDoesNotExist,
                    NotUniqueError,
                    SaveConditionError) as err:
                
                txt_message = "On %s examination: %s" % (str(i+1), err.message)
                logger.error(txt_message)
                message = Message(ExaminationErrorHeader(message=txt_message))
                return message
            
            logger.debug("Examination created: "+str(examination.data_inserimento))
            examination = self._get_examination(examination.id)
            examination.status = NewExaminationStatus(examination)
        
        # TODO: Return the list of created examinations
        
        if examination == None:
            message = "Examination already stored"
            examination = qs
        else:
            message = 'Examination created correctly'
        
        message = Message(ExaminationCorrectHeader(message=message),
                          data=examination)
        
        self._currentExamination = examination
        
        return message


    def read(self, **query):
        
        if 'data_inserimento' in query.keys():
            if isinstance(query['data_inserimento'], unicode):
                query['data_inserimento'] = datetime.strptime(query['data_inserimento'], 
                                                              "%Y-%m-%dT%H:%M:%S.%fZ" )
                
        if 'id_patient' in query.keys():
            query['id_patient'] = self._get_patient(str(query['id_patient']))
            
            
        if 'id_examination' in query.keys():
            query['id'] = query.pop('id_examination')
        
        
        logger.debug(query)
        
        examination = Examination.objects(**query)
        
        if examination.count() == 0:
            message = Message(ExaminationNoRecordHeader(),
                              data=examination)
            return message
        
        
        message = Message(ExaminationCorrectHeader(),
                          data=examination)
        return message
        
    
    def update(self, **query):
        # TODO: Check if examinatin
        
        return
    
    def delete(self, **query):   
        
        return
    
    
    def _pre_event(self, id_):
        qs_examination = self._get_examination(id_)
        examination = qs_examination.first()
        return qs_examination, examination
    
    
    def _update_technician(self, user, examination):
        
        query = dict()
        query['id_technician'] = User.objects(username=user).first()
        
        if not examination.modify(**query):
            message = Message(ExaminationErrorHeader(message='Error in modifying'))
            logger.error(message.header.message)
            return message
        
        # Try to save
        try:
            examination.save()
        except NotUniqueError, err:
            message = Message(ExaminationErrorHeader(message=err.message, 
                                                     user=self.user)) 
            logger.error(message.header.message)
            return message
        
    
    def _event_message(self, examination, qs):
        
        message_ = 'Examination is now %s' %(examination.status_name)
        logger.debug(message_)
        return Message(ExaminationCorrectHeader(message=message_),
                       data=qs)
    
    
    def start(self, **query):
        id_ = query['id']
        qs, examination = self._pre_event(id_)
        examination.status.start(examination)
        return self._event_message(examination, qs)
    
    
    def go(self, **query):
        id_ = query['id']
        qs, examination = self._pre_event(id_)
        examination.status.go(examination)
        return self._event_message(examination, qs)
    
    
    def stop(self, **query):
        id_ = query['id']
        qs, examination = self._pre_event(id_)
        examination.status.stop(examination)
        return self._event_message(examination, qs)
    
    
    def pause(self, **query):
        id_ = query['id']
        qs, examination = self._pre_event(id_)
        examination.status.pause(examination)
        return self._event_message(examination, qs)
    
    
    def finish(self, **query):
        id_ = query['id']
        qs, examination = self._pre_event(id_)
        self._update_technician(self.user, examination)
        examination.status.finish(examination)
        return self._event_message(examination, qs)
    
    
    def eject(self, **query):
        id_ = query['id']
        qs, examination = self._pre_event(id_)
        examination.status.eject(examination)
        return self._event_message(examination, qs)