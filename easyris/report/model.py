from mongoengine import *
from easyris.user.model import User
from easyris.examination.model import Examination
from easyris.report.status import  ReportStatus,\
    SuspendedReportStatus
from datetime import datetime
from easyris.base import EasyRisMixin, EasyRisQuerySet
from mongoengine.queryset import QuerySet
from mongoengine.dereference import DeReference


class ReportAction(EasyRisMixin, EmbeddedDocument):
    
    __collection__ = 'report_action'
    
    data =   DateTimeField(required=True, default=datetime.now())
    action = StringField(required=True)
    user =   ReferenceField(User, required=True)
    
    def _get_subfields(self, document):
        
        fields_ = {
                    'user':['username', 'first_name', 'last_name', 'roles']
                   }
        return document.to_mongo(fields=fields_[document.__collection__])


class Report(EasyRisMixin, Document):
    
    meta = {'queryset_class':EasyRisQuerySet}
    
    __collection__ = 'report'
    
    #datareferto
    id_examination =    ListField(ReferenceField(Examination))
    report_text =       StringField(required=True)
    status =            EmbeddedDocumentField(ReportStatus, default=SuspendedReportStatus())
    status_name =       StringField(required=True, default='suspended')
    action_list =       ListField(EmbeddedDocumentField(ReportAction))
    

    def _get_subfields(self, document):
                
        fields_ = {
                   'examination': ['id_typology', 
                                   'id_patient', 
                                   'id_technician', 
                                   'data_inserimento'],
                   'report_action': ['action', 'user', 'data']
                   }
        
        dereference = DeReference()
        document = dereference(document)

        return [d._to_easyris(fields=fields_[d.__collection__]) for d in document]

    