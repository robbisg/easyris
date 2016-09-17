from mongoengine import *
from easyris.user.model import User
from easyris.examination.model import Examination
from easyris.report.status import OpenReportStatus, ReportStatus


class Report(Document):
    __collection__ = 'report'

    id_examination = ListField(ReferenceField(Examination))
    report_text = StringField(required=True)
    status = EmbeddedDocumentField(ReportStatus, default=OpenReportStatus())
    status_name = StringField(required=True, default='open')
    doctor_list = ListField(ReferenceField(User))
    closed = BooleanField(default=False)
    #suspension_password
    
