from mongoengine import *
import unittest
from easyris.patient.model import Patient
from easyris.examination.model import Examination, \
                                    Priority, \
                                    Typology
from easyris.user.model import User
from datetime import datetime
from ...utils import patient_db, user_db, database_setup
from easyris.examination.status import NewExaminationStatus

#@unittest.skip("Not checked yet")
class TestExamination(unittest.TestCase):

    def setUp(self):
        
        database = 'test_easyris'
        port = 27017
        
        self.client = connect(database, port=port)
        database_setup.run(database, port, n_loaded=5)
        
        
    def tearDown(self):
        self.client.drop_database('test_easyris')
        return
    
    def test_model(self):
        print "---- Testing Examination ----"
        patient1 = Patient.objects(id_patient="2016020001").first()
        user1 = User.objects(username='gaetano').first()
        user2 = User.objects(username='daniele').first()
        
        typology = Typology.objects(modality='MR').first()
        
        priority = Priority.objects(priority_name='ALTA').first()
        
        examination = Examination(id_patient=patient1,
                         medico_richiedente='Pinco Pallo',
                         data_inserimento=datetime(year=2016, 
                                                   day=02, 
                                                   month=02),
                         id_priority=priority,
                         id_typology=typology,
                         id_creator=user1,
                         id_technician=user2,
                         accession_number='12345665',
                         codice_esenzione='67577568',
                         examination_note='ok'
                         )
        print '----------------------'
        examination.save()
        
        print '------ Object saved -----------'
        examination.status = NewExaminationStatus(examination)
        examination.status.start()
        assert examination.status_name == 'scheduled'
        examination.status.go()
        examination.status.pause()
        assert examination.status_name == 'incomplete'
        
        examination.status.start()
        examination.status.go()
        assert examination.status_name == 'running'
        
        examination.status.eject()
        examination.status.stop()
        assert examination.status_name == 'rescheduled'
        
        examination.status.start()
        assert examination.status_name == 'rescheduled'
        
        examination.status.go()
        examination.status.finish()
        assert examination.status_name == 'completed'
        
        examination.status.eject()
        assert examination.status_name == 'reported'
        
        



if __name__ == '__main__':
    unittest.run()
