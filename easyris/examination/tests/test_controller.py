from mongoengine import *
import unittest
from easyris.patient.model import Patient
from easyris.examination.model import Examination, \
                                    Priority, \
                                    Typology
from easyris.examination.controller import ExaminationController
from easyris.user.model import User
from datetime import datetime
from ...utils import patient_db, user_db, database_setup
from easyris.examination.status import NewExaminationStatus

#@unittest.skip("Not checked yet")
class TestExaminationController(unittest.TestCase):
    
    def setUp(self):
        
        database = 'test_easyris'
        port = 27017
        
        self.client = connect(database, port=port)
        database_setup.run(database, port, n_loaded=5)
        self.controller = ExaminationController()
        
        
    def tearDown(self):
        self.client.drop_database('test_easyris')
        return
    

    def test_create(self):
        
        user = User.objects(username='gaetano').first()
        self.controller.user = user
        query = dict()
        
        priority = Priority.objects(priority_name='ROUTINE').first()
        technician = User.objects(username='daniele').first()
        typology = Typology.objects(codice_regionale='RM11').first()
        
        
        query['id_priority'] = str(priority.priority_name) # Routine
        query['id_technician'] = str(technician.id) # Daniele-Tecnico
        query['id_typology'] = str(typology.id) # RM Encefalo senza mdc
        query['id_patient'] = "2016080001"
        query['medico_richiedente'] = 'Mauro Caffarini'
        query['accession_number'] = '11111111'
        query['data_inserimento'] = "1983-05-18T13:08:00.0Z"
        
        message = self.controller.create(**query)
        print message.header.message
        self.assertEqual(message.header.code, 200)
    
    
    #@unittest.skip("Not checked yet")
    def test_read(self):
        
        query = dict()
        query['medico_richiedente'] = 'Mauro Caffarini'
        message = self.controller.read(**query)
        examination = message.data.first()
        
        assert examination['codice_esenzione'] == '67577568'
        
    
    
    @unittest.skip("Not checked yet")
    def test_update(self):
        return


    @unittest.skip("Not checked yet")
    def test_delete(self):       
        return
    
    #@unittest.skip("Not checked yet")
    def test_status(self):
        
        query = dict()
        query['medico_richiedente'] = 'Mauro Caffarini'
        message = self.controller.read(**query)
        examination = message.data.first()
        
        m = self.controller.start(id=str(examination.id))
        examination = m.data.first()
        assert examination.status_name == 'scheduled'
        
        m = self.controller.go(id=str(examination.id))
        examination = m.data.first()
        assert examination.status_name == 'running'
        
        m = self.controller.stop(id=str(examination.id))
        examination = m.data.first()
        assert examination.status_name == 'rescheduled'
        
        m = self.controller.go(id=str(examination.id))
        examination = m.data.first()
        m = self.controller.pause(id=str(examination.id))
        examination = m.data.first()
        assert examination.status_name == 'incomplete'
        m = self.controller.stop(id=str(examination.id))
        examination = m.data.first()
        assert examination.status_name == 'incomplete'
                                 
        m = self.controller.start(id=str(examination.id))
        examination = m.data.first()
        m = self.controller.go(id=str(examination.id))
        examination = m.data.first()
        m = self.controller.finish(id=str(examination.id))
        examination = m.data.first()
        assert examination.status_name == 'completed'
        
        m = self.controller.eject(id=str(examination.id))
        examination = m.data.first()
        assert examination.status_name == 'reported'