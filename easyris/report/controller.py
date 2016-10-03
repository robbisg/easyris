import numpy as np
from mongoengine import *
from easyris.report.model import Report, ReportAction
from easyris.user.model import User
from easyris.base.message.message import Message
from easyris.user.message import UserNotHavingRole
from easyris.report.message import ReportActionForbidden, ReportErrorHeader,\
    ReportCorrectHeader
from easyris.examination.model import Examination
from easyris.user.controller import PermissionController

import logging
logger = logging.getLogger('easyris_logger')

class ReportController(object):
    
    _permission = PermissionController()
    
    def __init__(self, name='report', user=None):
        self._currentReport = None
        self.name = name
        self.user = user
        return
    
    def _get_report(self, id_report):
        """Deprecated: to be subsituted with a function in a superclass"""
        report = Report.objects(id=str(id_report))
        
        if report == None:
            logger.error("No report in the database")
            return 'ERR'
        
        self._currentReport = report.first()
        return report
    
    
    def _check_fields(self, query):
        
        for key in query.keys():
            
            if key == 'user':
                
                if isinstance(query[key], User):
                    user = query[key]
                else:
                    user = User.objects(username=query[key]).first()
                    
                is_medico = False
                for r in user.roles:
                    if r.role_name == 'medico':
                        is_medico = True
                        query['user'] = user
                        break
                
                
                if is_medico:
                    query[key] = user
                else:
                    query[key] = Message(header=UserNotHavingRole(),
                                         data=None)
            
            elif key == 'action':
                
                if not query[key] in ['create', 'close', 'open', 'update']:
                    query[key] = Message(header=ReportActionForbidden(action=key),
                                         data=None)
                
            
            elif key == 'id_examination':
                query[key] = self._check_examination(query[key])
                logger.debug(query[key])
                
            elif key == 'report_text':
                continue
            
            elif key == 'id':
                continue
            
            else:
                _ = query.pop(key)
                
            
            if isinstance(query[key], Message):
                return query[key]
            
        
        return query
    
    
    def _check_examination(self, list_id_examinations):

        examination_list = Examination.objects(id__in=list_id_examinations)
        filter_ = np.unique([(e.id_patient.id, 
                              e.data_inserimento, 
                              e.status_name) for e in examination_list])
        

        if filter_.shape[0] > 3:
            message = "Examinations are from different patient or date"
            return Message(ReportErrorHeader(message=message),
                           data=None)
        
        if filter_[2] != 'completed':
            message = "Examinations are not completed"
            return Message(ReportErrorHeader(message=message),
                           data=None)
            
        return examination_list
    
    
    def _create_action(self, query):
        
        action = query.pop('action')
        user = query.pop('user')
        
        report_action = ReportAction(user=user, 
                                     action=action)
        
        return report_action
    
    def create(self, **query):
        
        query['user'] = self.user
        
        query = self._check_fields(query)    
        
        if isinstance(query, Message):
            return query      
        
        query['action_list'] = [self._create_action(query)]
        
        if isinstance(query['action_list'], Message):
            return query['action_list']        
        
        query['id_patient'] = query['id_examination'][0].id_patient.id_patient
        
        logger.debug(query)
        
        report = Report(**query)
        
        try:
            report.save()
        except (FieldDoesNotExist,
                NotUniqueError,
                SaveConditionError) as err:
                
            txt_message = "Report cannot be saved: %s " % (err.message)
            logger.error(txt_message)
            message = Message(ReportErrorHeader(message=txt_message))
            return message
        
        
        self._currentReport = report
        
        message = "Report correctly created"
        report = Report.objects(id=report.id)
        message = Message(ReportCorrectHeader(message=message),
                          data=report)
        
        return message
    


    def read(self, **query):
        
        # TODO: Check fields
        
        logger.debug(query)
        
        report = Report.objects(**query)
        
        if report.count() == 0:
            message = Message(ReportErrorHeader(message="No Reports in database"),
                              data=report)
            return message
                
        message = Message(ReportCorrectHeader(message="Reports loaded"),
                          data=report)
        return message
        
        
    
    def update(self, **query):
        
        query['user'] = self.user
        
        query = self._check_fields(query)    
        
        if isinstance(query, Message):
            return query     
        
        logger.debug(query)
        
        action = query.pop('action')
        user = query.pop('user')
        id_report = query.pop('id')
        
        report = self._get_report(id_report).first()
        
        if not report.modify(**query):
            message = Message(ReportErrorHeader(message='Error in modifying'))
            logger.error(message.header.message)
            return message
        
        message = self._update_log(user, action, report)

        if message != None:
            return message
        
        self._currentReport = report
                
        report = Report.objects(**query)
        message = "Report correctly updated"
        message = Message(ReportCorrectHeader(message=message),
                          data=report)

        return message  
        
    
    def delete(self, **query):       
        
        return     
        
    
    def _pre_event(self, id_):
        qs_report = self._get_report(id_)
        report = qs_report.first()
        return qs_report, report
    
    
    def _event_message(self, examination, qs):
        
        message_ = 'Report is now %s' %(examination.status_name)
        return Message(ReportCorrectHeader(message=message_),
                       data=qs)
    
    
    def _check(self, username, password):
        message = self._permission.login(username, password)
        return message.data['is_authenticated']
        
    
    def _check_status(self, report, status):
        
        if report.status_name != status:
            text = "Report is not %s" % (status)
            message = Message(ReportErrorHeader(message=text, 
                                                     user=self.user))
            return message
        
        return None
        
    
    
    def _update_log(self, user, action, report):
        
        query_action = dict()
        query_action['user'] = user
        query_action['action'] = action
        
        query_action = self._check_fields(query_action)
        
        if isinstance(query_action, Message):
            return query_action
        
        report.action_list.append(self._create_action(query_action))
        
        try:
            report.save()
        except NotUniqueError, err:
            message = Message(ReportErrorHeader(message=err.message, 
                                                     user=self.user)) 
            logger.error(message.header.message)
            return message
        
        return None
        
        
    def open(self, **query):
                
        id_ = query['id']
        qs, report = self._pre_event(id_)
        
        # TODO: Move this to ReportStatus class?
        transition = self._check_status(report, 'closed')
        if transition != None:
            return transition        
        
        password = query['password']
        username = self.user
        
        if not self._check(username, password) or \
                report.action_list[-1].user.username != self.user:
            text = "%s not allowed to open this report" % (self.user)
            message = Message(ReportErrorHeader(message=text, 
                                                     user=self.user))
            return message
        
        report.status.open(report)
        self._update_log(self.user, 'open', report)
        
        return self._event_message(report, qs)
    
    
    
    def close(self, **query):

        id_ = query['id']
        qs, report = self._pre_event(id_)       
        
        transition = self._check_status(report, 'suspended')
        if transition != None:
            return transition
        
        report.status.close(report)
        self._update_log(self.user, 'close', report)
        
        return self._event_message(report, qs)

    
    def print_report(self, **query):
        # Get information about the report
        # Pack into the Message
        # Send it to controller
        id_ = query['id']
        _, report = self._pre_event(id_)
                
        data = dict()
        data['patient.first_name'] = report.id_examination[0].id_patient.first_name
        data['patient.last_name'] = report.id_examination[0].id_patient.last_name
        data['patient.birth_date'] = report.id_examination[0].id_patient.birthdate
        data['examination.date'] = report.id_examination[0].data_inserimento
        data['examination.tecnico.first_name'] = report.id_examination[0].id_technician.first_name
        data['examination.tecnico.last_name'] = report.id_examination[0].id_technician.last_name
        data['text'] = report.report_text
        data['status'] = report.status_name
        data['medico.first_name'] = report.action_list[-1].user.first_name
        data['medico.last_name'] = report.action_list[-1].user.last_name
        data['is_modified'] = True
        for action in report.action_list[::-1]:
            if action.action == 'open':
                data['is_modified'] = True
                data['open_data'] = action.data
        
        message = Message(ReportCorrectHeader(message='Printing Report', 
                                              user=self.user),
                          data = data
                          )
        logger.debug(message.header.message)
        logger.debug(message.data)
        return message