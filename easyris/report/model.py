from mongoengine import *
from easyris.user.model import User
from easyris.examination.model import Examination
from easyris.report.status import OpenReportStatus, ReportStatus

# TODO: Inserire invece di doctor_list e date varie
# TODO: Una nuova referenza a un campo ReportActionLog
# TODO: con azione, data, medico
class ReportActionLog(EmbeddedDocument):
    
    action = StringField(required=True)
    data = DateTimeField(required=True)
    user = ReferenceField(User)
    # Check if it is a medico




class Report(Document):
    __collection__ = 'report'
    
    #datareferto
    id_examination =    ListField(ReferenceField(Examination))
    report_text =       StringField(required=True)
    status =            EmbeddedDocumentField(ReportStatus, default=OpenReportStatus())
    status_name =       StringField(required=True, default='open')
    action_list =       ListField(EmbeddedDocumentField(ReportActionLog))
    



    