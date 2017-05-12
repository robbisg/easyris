from mongoengine import *
from qScience.model.user import User
from qScience.model.examination import Examination
from qScience.model.report_status import  ReportStatus,\
    SuspendedReportStatus, OpenedReportStatus
from datetime import datetime
from qScience.base import QScienceMixin, QScienceQuerySet
from mongoengine.queryset import QuerySet
from mongoengine.dereference import DeReference


class ReportAction(QScienceMixin, EmbeddedDocument):
    
    __collection__ = 'report_action'
    
    data =   DateTimeField(required=True, default=datetime.now())
    action = StringField(required=True)
    user =   ReferenceField(User, required=True)
    
    def _get_subfields(self, document):
        
        fields_ = {
                    'user':['username', 'first_name', 'last_name', 'roles']
                   }
        
        return document.to_mongo(fields=fields_[document.__collection__])


class Report(QScienceMixin, Document):
    
    meta = {'queryset_class':QScienceQuerySet}
    
    __collection__ = 'report'
    
    #datareferto
    id_examination =    ListField(ReferenceField(Examination))
    report_text =       StringField(required=True)
    status =            EmbeddedDocumentField(ReportStatus, default=OpenedReportStatus())
    status_name =       StringField(required=True, default='opened')
    action_list =       ListField(EmbeddedDocumentField(ReportAction))
    id_patient =        StringField(required=True)
    

    def _get_subfields(self, document):
                
        fields_ = {
                   'examination': ['id_typology', 
                                   'id_patient', 
                                   'id_technician', 
                                   'data_inserimento',
                                   'status_name'],
                   'report_action': ['action', 'user', 'data']
                   }
        

        dereference = DeReference()
        document = dereference(document)

        return [d._to_easyris(fields=fields_[d.__collection__]) for d in document]

    