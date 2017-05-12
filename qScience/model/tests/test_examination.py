from mongoengine import *
import unittest
from qScience.model.patient import Patient
from qScience.model.examination import Examination, \
                                    Priority, \
                                    Typology
from qScience.model.user import User
from datetime import datetime
from qScience.tests.test import EasyRisUnitTest

#@unittest.skip("Not checked yet")
class TestExamination(EasyRisUnitTest):
        
            
    def test_model(self):
        print "---- Testing Examination ----"
        patient1 = Patient.objects(first_name="Tecla").first()
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
        assert examination.status.name == 'new'
        
        print '------ Object saved -----------'
        examination.status.start(examination)
        assert examination.status_name == 'scheduled'
        examination.status.go(examination)
        examination.status.pause(examination)
        assert examination.status_name == 'incomplete'
        
        examination.status.start(examination)
        examination.status.go(examination)
        assert examination.status_name == 'running'
        
        examination.status.eject(examination)
        examination.status.stop(examination)
        assert examination.status_name == 'rescheduled'
        
        examination.status.start(examination)
        assert examination.status_name == 'rescheduled'
        
        examination.status.go(examination)
        examination.status.finish(examination)
        assert examination.status_name == 'completed'
        
        examination.status.eject(examination)
        assert examination.status_name == 'reported'
        
    def test_accession_number(self):
        print "---- Testing Examination ----"
        patient1 = Patient.objects(first_name="Tecla").first()
        user1 = User.objects(username='gaetano').first()
        user2 = User.objects(username='daniele').first()
        
        typology_qs = Typology.objects(room='RM1.5T',
                                    distretto_corporeo='TESTA/COLLO')
        
        typology1 = typology_qs[0]
        typology2 = typology_qs[1]
        
        
        assert typology1.examination_name != typology2.examination_name
        
        priority = Priority.objects(priority_name='ALTA').first()
        
        examination1 = Examination(id_patient=patient1,
                                  medico_richiedente='Pinco Pallo',
                                  data_inserimento=datetime(year=2016, 
                                                            day=05, 
                                                            month=02),
                                  id_priority=priority,
                                  id_typology=typology1,
                                  id_creator=user1,
                                  id_technician=user2,
                                  #accession_number='12345665',
                                  codice_esenzione='67577568',
                                  examination_note='ok'
                                  )
        
        examination2 = Examination(id_patient=patient1,
                                  medico_richiedente='Pinco Pallo',
                                  data_inserimento=datetime(year=2016, 
                                                            day=05, 
                                                            month=02),
                                  id_priority=priority,
                                  id_typology=typology2,
                                  id_creator=user1,
                                  id_technician=user2,
                                  #accession_number='12345665',
                                  codice_esenzione='67577568',
                                  examination_note='ok'
                                  )        
        
        examination1.save()
        examination2.save()
        
        assert examination1.accession_number == examination2.accession_number
        
        examination3 = Examination(id_patient=patient1,
                                  medico_richiedente='Pinco Pallo',
                                  data_inserimento=datetime(year=2016, 
                                                            day=05, 
                                                            month=03),
                                  id_priority=priority,
                                  id_typology=typology2,
                                  id_creator=user1,
                                  id_technician=user2,
                                  #accession_number='12345665',
                                  codice_esenzione='67577568',
                                  examination_note='ok'
                                  )        
        examination3.save()
        
        assert examination2.accession_number != examination3.accession_number
        
        
        return
