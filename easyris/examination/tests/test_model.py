from mongoengine import *
import unittest
from easyris.patient.model import Patient
from easyris.examination.model import Examination, PriorityEmbedded, ExamStatusEmbedded, TypologyEmbedded
from datetime import datetime

# from ..controller import ExaminationController
# from ...utils import patient_db

# @unittest.skip("showing class skipping")

@unittest.skip("Not checked yet")
class TestExamination(unittest.TestCase):

    def setUp(self):
        connect('easyris', port=27017)
        Examination.drop_collection()
        # patient_db.run(n_loaded=5)

    def test_model(self):
        print "Testing model"
        patient1 = Patient.objects(id_patient="2016020001").first()
        me = Examination(id_patient=patient1.id,
                         medico_richiedente='Pinco Pallo',
                         data_inserimento=datetime(year=2016, day=02, month=02),
                         id_priority=PriorityEmbedded(priority_name="ALTA"),
                         id_exam_status=ExamStatusEmbedded(exam_status_name="PRENOTATO"),
                         id_typology=TypologyEmbedded(modality="MR", room="RM1.5T",
                                                      distretto_corporeo="TESTA/COLLO",
                                                      exam_name="RM ENCEFALO SENZA MDC",
                                                      descrizione_ministeriale="Risonanza magnetica nucleare \
                                                      (rm) del cervello e del tronco encefalico")
                         # id_creator="3294946261",
                         # id_report
                         # id_technician='piero.chiacchiaretta@gmail.com',
                         # accession_number='12345665',
                         # codice_esenzione='67577568',
                         # examination_note='ok')
                         )
        me.save()

        examination_ins = Examination.objects(medico_richiedente='Pinco Pallo').first()
        assert examination_ins.data_inserimento == datetime(year=2016, day=02, month=02)
        # altri controlli


if __name__ == '__main__':
    unittest.run()
