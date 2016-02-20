from mongoengine import *
import unittest
from easyris.patient.model import Patient
from easyris.report.model import Report, ReportStatusEmbedded, ReportStatus
from easyris.examination.model import Examination, PriorityEmbedded, ExamStatusEmbedded, TypologyEmbedded


# from ..controller import ExaminationController
# from ...utils import patient_db

# @unittest.skip("showing class skipping")

# TODO FAR VEDERE A ROBERTO COME PROCEDERE PER I VARI UNITEST SUL REFERTO

class TestExamination(unittest.TestCase):

    def setUp(self):
        connect('easyris', port=27017)
        Report.drop_collection()
        # patient_db.main(n_loaded=5)

    def test_model(self):
        print "Testing model"
        patient1 = Patient.objects(id_patient="2016020001").first()
        examination1 = Examination.objects(id_patient="2016020001").first()
        me = Report(id_patient=patient1.id,
                    id_examination=examination1.id,
                    report_text='Pinco Pallo',
                    )
        me.save()

        report_ins = Report.objects(report_text='Pinco Pallo').first()
        assert report_ins.report_text == 'Pinco Pallo'
        # altri controlli


if __name__ == '__main__':
    unittest.main()
