from mongoengine import *
import unittest
from qScience.model.user import User
from qScience.model.examination import Priority
from qScience.controller.examination import ExaminationController
from qScience.tests.test import EasyRisUnitTest
from datetime import datetime


#@unittest.skip("Not checked yet")
class TestExaminationController(EasyRisUnitTest):
    
    def setUp(self):
        
        self.controller = ExaminationController()
        super(TestExaminationController, self).setUp()
            

    def test_create(self):
        
        user = User.objects(username='gaetano').first()
        self.controller.user = user
        query = dict()
        
        priority = Priority.objects(priority_name='ROUTINE').first()
        technician = User.objects(username='daniele').first()
        #typology = Typology.objects(codice_regionale='RM11').first()
        
        query['id_creator'] = str(user.username)
        query['id_priority'] = str(priority.priority_name) # Routine
        query['id_technician'] = str(technician.id) # Daniele-Tecnico
        query['exams'] =  [{"priority":"ALTA",
                            "modality":"MR",
                            "sala":"RM1.5T",
                            "distretto":"TORACE",
                            "nome":"RM TORACE SENZA MDC",
                            "selected":True}]
        query['id_patient'] = "2016120001"
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
        
    
    
    @unittest.skip("Not implemented yet")
    def test_update(self):
        return


    @unittest.skip("Not implemented yet")
    def test_delete(self):       
        return
    
    #@unittest.skip("Not checked yet")
    def test_status(self):
        
        query = dict()
        #today = datetime.now()
        query['data_inserimento'] = unicode(datetime(day=10,
                                                     month=12,
                                                     year=2016).isoformat()+
                                            '.0Z')
        query['status_name'] = 'new'
        message = self.controller.read(**query)
        examination = message.data.first()
        print examination
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