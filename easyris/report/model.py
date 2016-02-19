from mongoengine import *
# from easyris.user.model import User
from easyris.patient.model import Patient
from easyris.examination.model import Examination


class ReportStatus(Document):
    __collection__ = 'report_status'

    report_status = StringField(required=True)


class ReportStatusEmbedded(EmbeddedDocument):
    __collection__ = 'report_status'

    report_status = StringField(required=True)


class Report(Document):
    __collection__ = 'report'

    id_patient = ReferenceField(Patient)
    id_examination = EmbeddedDocumentField(Examination)
    report_text = StringField(required=True)
    id_report_status = EmbeddedDocumentField(ReportStatusEmbedded)
    # doctor_list = ReferenceField(User)
    


