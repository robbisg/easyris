from mongoengine import *
# from easyris.user.model import User
from easyris.patient.model import Patient
from easyris.examination.model import Examination


class ReportStatus(Document):
    __collection__ = 'report_status'

    status = StringField(required=True)



class Report(Document):
    __collection__ = 'report'

    id_patient = ReferenceField(Patient)
    id_examination = ReferenceField(Examination)
    report_text = StringField(required=True)
    id_status = ReferenceField(ReportStatus)
    # doctor_list = ReferenceField(User)
    


